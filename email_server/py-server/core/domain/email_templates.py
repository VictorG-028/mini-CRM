



DISCOUNT_CUPOM_TEMPLATE = """
<html>
<head>
    <style>
        /* Estilos para clientes de e-mail que suportam <style>, como o Gmail */
        body {{
            font-family: Arial, Helvetica, sans-serif;
        }}
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td style="padding: 20px 0 30px 0;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; background-color: #ffffff; border: 1px solid #cccccc; border-radius: 8px; overflow: hidden;">
                    <tr>
                        <td align="center">
                            <img src="cid:promo_header" alt="Promoção Imperdível!" width="600" style="display: block; width: 100%; max-width: 600px; height: auto;"/>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 30px 40px 40px 40px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; text-align: center;">
                                        Um presente para você!
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 20px 0 20px 0; color: #555555; font-family: Arial, sans-serif; font-size: 16px; line-height: 24px; text-align: center;">
                                        Você recebeu um cupom de desconto exclusivo. Mostre ou informe o código abaixo para um atendente e aproveite!
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <p style="font-family: Arial, sans-serif; font-size: 16px; margin: 10px 0;"><strong>Seu código:</strong></p>
                                        <p style="background-color: #e0f2ff; border: 2px dashed #007bff; padding: 12px 24px; font-size: 22px; font-family: 'Courier New', Courier, monospace; font-weight: bold; color: #0056b3; display: inline-block; border-radius: 8px;">
                                            {cupom_code}
                                        </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 20px 0 0 0; color: #777777; font-family: Arial, sans-serif; font-size: 14px; line-height: 20px; text-align: center;">
                                        Use seu desconto de <strong>{discount_value}</strong> entre os dias {start_date} e {end_date}.
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                </td>
        </tr>
    </table>
</body>
</html>
"""
