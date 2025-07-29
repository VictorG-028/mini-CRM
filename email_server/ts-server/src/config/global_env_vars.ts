import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();


const smtpConfigSchema = z.object({
  GOOGLE_SENDER_EMAIL: z.email('GOOGLE_SENDER_EMAIL deve ser um e-mail válido.'),
  GOOGLE_SENDER_PASSWORD: z.string().min(1, 'GOOGLE_SENDER_PASSWORD é obrigatório.'),
  SMTP_SERVER: z.string().min(1, 'SMTP_SERVER é obrigatório.'),
  SMTP_PORT: z.preprocess(
    (val) => parseInt(val as string, 10), // Converte para número
    z.number().int().positive('SMTP_PORT deve ser um número inteiro positivo.')
  ),
});

const supabaseConfigSchema = z.object({
  SUPABASE_URL: z.url('SUPABASE_URL deve ser uma URL válida.'),
  SUPABASE_SECRET_KEY: z.string().min(1, 'SUPABASE_SECRET_KEY é obrigatório.'),
});

const mongoAtlasConfigSchema = z.object({
  MONGO_URI: z.url('MONGO_URI deve ser uma URL de conexão válida para MongoDB.'),
  MONGO_DB_USER: z.string().min(1, 'MONGO_DB_USER é obrigatório.'),
  MONGO_DB_PASSWORD: z.string().min(1, 'MONGO_DB_PASSWORD é obrigatório.'),
  MONGO_DB_CODE: z.string().optional(), // Assumindo que DB_CODE pode ser opcional se não for usado
  MONGO_DB_NAME: z.string().min(1, 'MONGO_DB_NAME é obrigatório.'),
});


const adminControlsSchema = z.object({
  SERVER_PORT: z.preprocess(
    (val) => parseInt(val as string, 10),
    z.number().int().positive('SERVER_PORT deve ser um número inteiro positivo.')
  ),
  DATABASE_TYPE: z.enum(["mongodb", "supabase"], 'DATABASE_TYPE deve ser "mongodb" ou "supabase".'),
  EMAIL_SENDER: z.string().min(1, 'EMAIL_SENDER é obrigatório.'),
  IS_PROD: z.preprocess(
    (val) => String(val).toLowerCase() === 'true',
    z.boolean()
  ),
});

type EnvVars = z.infer<typeof smtpConfigSchema> &
  z.infer<typeof supabaseConfigSchema> &
  z.infer<typeof mongoAtlasConfigSchema> &
  z.infer<typeof adminControlsSchema>;

const envSchema = smtpConfigSchema
  .extend(supabaseConfigSchema.shape)
  .extend(mongoAtlasConfigSchema.shape)
  .extend(adminControlsSchema.shape);

let parsedEnv: EnvVars;

try {
  parsedEnv = envSchema.parse(process.env);
} catch (error) {

  if (error instanceof z.ZodError) {
    console.error('❌ Erro de validação de variáveis de ambiente:');
    for (const issue of error.issues) {
      console.error(`- Campo: ${issue.path.join('.') || 'Desconhecido'} | Mensagem: ${issue.message}`);
    }
  } else {
    console.error('❌ Erro inesperado ao carregar variáveis de ambiente:', error);
  }
  process.exit(1);

}

export const global_env_vars = parsedEnv;

console.log('✅ Variáveis de ambiente carregadas e validadas com sucesso!');
if (!global_env_vars.IS_PROD) {
  console.log('Ambiente de desenvolvimento. Configurações:');
  console.log(JSON.stringify(global_env_vars, null, 2));
}
