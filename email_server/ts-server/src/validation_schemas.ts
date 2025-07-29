import { z } from 'zod';

export const SendEmailRequestSchema = z.object({
  to: z.email('Formato de e-mail inválido.').min(1, 'Destinatário é obrigatório.'),
  subject: z.string().min(1, 'Assunto é obrigatório.'),
  body: z.string().min(1, 'Corpo do e-mail é obrigatório.'),
});
export type SendEmailRequest = z.infer<typeof SendEmailRequestSchema>;
