// src/app.ts
import express, { Request, Response } from 'express';
import EmailService from './email_service';
import { SendEmailRequestSchema } from './validation_schemas';
import { ZodError } from 'zod'; // Importa ZodError para tratamento de erros
import { global_env_vars } from './config/global_env_vars';

const app = express();


app.use(express.json());

app.post('/emails/send-emails', async (req: Request, res: Response) => {
  try {
    const emailData = SendEmailRequestSchema.parse(req.body);

    const success = await EmailService.sendEmail(emailData);

    if (success) {
      return res.status(200).json({ message: 'E-mail enviado com sucesso!' });
    } else {
      return res.status(500).json({ message: 'Falha ao enviar e-mail.' });
    }
  } catch (error) {
    if (error instanceof ZodError) {
      console.error('Erro de validação de input:', error.issues);
      return res.status(422).json({
        message: 'Dados de requisição inválidos.',
        errors: error.issues.map(err => ({ path: err.path, message: err.message }))
      });
    }

    console.error('Erro inesperado:', error);
    return res.status(500).json({ message: 'Ocorreu um erro interno no servidor.' });
  }
});

app.get('/', (req: Request, res: Response) => {
  res.send('Servidor de e-mails rodando!');
});

app.listen(global_env_vars.SERVER_PORT, () => {
  console.log(`Servidor Express rodando na porta ${global_env_vars.SERVER_PORT}`);
  if (global_env_vars.IS_PROD) {
    console.log('Ambiente de produção detectado.');
    console.log(`Acesse: http://localhost:${global_env_vars.SERVER_PORT}`);
  }
});

