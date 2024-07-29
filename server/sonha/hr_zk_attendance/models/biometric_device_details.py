# -*- coding: utf-8 -*-
import datetime
import logging
import pytz
from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)
try:
    from zk import ZK, const
except ImportError:
    _logger.error("Please Install pyzk library.")


class BiometricDeviceDetails(models.Model):
    """Model for configuring and connect the biometric device with odoo"""
    _name = 'biometric.device.details'
    _description = 'Biometric Device Details'

    name = fields.Char(string='Name', required=True, help='Record Name')
    device_ip = fields.Char(string='Device IP', required=True,
                            help='The IP address of the Device')
    port_number = fields.Integer(string='Port Number', required=True,
                                 help="The Port Number of the Device")
    address_id = fields.Many2one('res.partner', string='Working Address',
                                 help='Working address of the partner')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda
                                     self: self.env.user.company_id.id,
                                 help='Current Company')

    def device_connect(self, zk):
        """Function for connecting the device with Odoo"""
        try:
            conn = zk.connect()
            return conn
        except Exception:
            return False

    def action_test_connection(self):
        """Checking the connection status"""
        zk = ZK(self.device_ip, port=self.port_number, timeout=30,
                password=False, ommit_ping=False)
        try:
            if zk.connect():
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'Successfully Connected',
                        'type': 'success',
                        'sticky': False
                    }
                }
        except Exception as error:
            raise ValidationError(f'{error}')

    def action_clear_attendance(self):
        """Methode to clear record from the zk.machine.attendance model and
        from the device"""
        for info in self:
            try:
                machine_ip = info.device_ip
                zk_port = info.port_number
                try:
                    # Connecting with the device
                    zk = ZK(machine_ip, port=zk_port, timeout=30,
                            password=0, force_udp=False, ommit_ping=False)
                except NameError:
                    raise UserError(_(
                        "Please install it with 'pip3 install pyzk'."))
                conn = self.device_connect(zk)
                if conn:
                    conn.enable_device()
                    clear_data = zk.get_attendance()
                    if clear_data:
                        # Clearing data in the device
                        conn.clear_attendance()
                        # Clearing data from attendance log
                        self._cr.execute(
                            """delete from zk_machine_attendance""")
                        conn.disconnect()
                    else:
                        raise UserError(
                            _('Unable to clear Attendance log.Are you sure '
                              'attendance log is not empty.'))
                else:
                    raise UserError(
                        _('Unable to connect to Attendance Device. Please use '
                          'Test Connection button to verify.'))
            except Exception as error:
                raise ValidationError(f'{error}')

    def action_download_attendance(self):
        """Function to download attendance records from the device"""
        _logger.info("++++++++++++Cron Executed++++++++++++++++++++++")
        zk_attendance = self.env['zk.machine.attendance']
        hr_attendance = self.env['hr.attendance']
        for info in self:
            machine_ip = info.device_ip
            zk_port = info.port_number
            try:
                # Connecting with the device with the ip and port provided
                zk = ZK(machine_ip, port=zk_port, timeout=15,
                        password=0,
                        force_udp=False, ommit_ping=False)
            except NameError:
                raise UserError(
                    _("Pyzk module not Found. Please install it"
                      "with 'pip3 install pyzk'."))
            conn = self.device_connect(zk)
            if conn:
                conn.disable_device()
                users = conn.get_users()
                attendances = conn.get_attendance()
                if attendances:
                    # Thu thập dữ liệu chấm công theo nhân viên và ngày
                    attendance_by_employee_date = {}
                    for each in attendances:
                        atten_time = each.timestamp
                        if atten_time.year == 2024:
                            date_key = atten_time.date()
                            user_key = each.user_id
                            if (user_key, date_key) not in attendance_by_employee_date:
                                attendance_by_employee_date[(user_key, date_key)] = {'check_in': None,
                                                                                     'check_out': None}
                            if each.punch == 0:  # check-in
                                attendance_by_employee_date[(user_key, date_key)]['check_in'] = atten_time
                            elif each.punch == 1:  # check-out
                                attendance_by_employee_date[(user_key, date_key)]['check_out'] = atten_time

                    # Xử lý dữ liệu chấm công đã thu thập
                    for user in users:
                        user_key = user.user_id
                        employee = self.env['hr.employee'].search([('device_id_num', '=', user_key)])
                        if not employee:
                            employee = self.env['hr.employee'].create({
                                'device_id_num': user_key,
                                'name': user.name
                            })

                        for date_key in attendance_by_employee_date.keys():
                            if (user_key, date_key) in attendance_by_employee_date:
                                times = attendance_by_employee_date[(user_key, date_key)]
                                check_in_time = times['check_in']
                                check_out_time = times['check_out']

                                if check_in_time and check_out_time:
                                    local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')

                                    local_check_in = local_tz.localize(check_in_time, is_dst=None)
                                    utc_check_in = local_check_in.astimezone(pytz.utc)
                                    check_in_str = utc_check_in.strftime("%Y-%m-%d %H:%M:%S")
                                    check_in_time = fields.Datetime.to_string(
                                        datetime.datetime.strptime(check_in_str, "%Y-%m-%d %H:%M:%S"))

                                    local_check_out = local_tz.localize(check_out_time, is_dst=None)
                                    utc_check_out = local_check_out.astimezone(pytz.utc)
                                    check_out_str = utc_check_out.strftime("%Y-%m-%d %H:%M:%S")
                                    check_out_time = fields.Datetime.to_string(
                                        datetime.datetime.strptime(check_out_str, "%Y-%m-%d %H:%M:%S"))

                                    # Đảo ngược thời gian nếu cần thiết
                                    if check_out_time < check_in_time:
                                        check_in_time, check_out_time = check_out_time, check_in_time

                                    hr_attendance.create({
                                        'employee_id': employee.id,
                                        'check_in': check_in_time,
                                        'check_out': check_out_time
                                    })
                    conn.disconnect()
                    return True
                else:
                    raise UserError(_('Unable to get the attendance log, please try again later.'))
            else:
                raise UserError(_('Unable to connect, please check the parameters and network connections.'))

    def action_restart_device(self):
        """For restarting the device"""
        zk = ZK(self.device_ip, port=self.port_number, timeout=15,
                password=0,
                force_udp=False, ommit_ping=False)
        self.device_connect(zk).restart()
