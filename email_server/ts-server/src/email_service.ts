import nodemailer from 'nodemailer';
import { SendEmailRequest } from './validation_schemas';
import { global_env_vars } from './config/global_env_vars';

const GOOGLE_SENDER_EMAIL = global_env_vars.GOOGLE_SENDER_EMAIL;
const GOOGLE_SENDER_PASSWORD = global_env_vars.GOOGLE_SENDER_PASSWORD;
const SMTP_SERVER = global_env_vars.SMTP_SERVER;
const SMTP_PORT = global_env_vars.SMTP_PORT;

const transporter = nodemailer.createTransport({
  service: 'gmail',
  host: SMTP_SERVER,
  port: SMTP_PORT,
  secure: SMTP_PORT === 465,
  auth: {
    user: GOOGLE_SENDER_EMAIL,
    pass: GOOGLE_SENDER_PASSWORD,
  },
});

export default class EmailService {

  static async sendEmail(emailData: SendEmailRequest): Promise<boolean> {
    try {
      const info = await transporter.sendMail({
        from: `${GOOGLE_SENDER_EMAIL}`,
        to: emailData.to,
        subject: emailData.subject,
        html: emailData.body,
      });

      console.log(`E-mail enviado para: ${emailData.to}`);
      console.log(`ID da mensagem: ${info.messageId}`);
      return true;
    } catch (error) {
      console.error(`Erro ao enviar e-mail para ${emailData.to}:`, error);
      return false;
    }
  }

}
