import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

import 'clinic_color_palette.dart';

class FormPage extends StatefulWidget {
  const FormPage({super.key});

  @override
  State<FormPage> createState() => _FormPageState();
}

class _FormPageState extends State<FormPage> {
  final _formKey = GlobalKey<FormState>();
  final _userFullNameCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _telephoneCtrl = TextEditingController();
  final _cpfCtrl = TextEditingController();
  final _birthDateCtrl = TextEditingController();
  DateTime? _selectedBirthDate;

  bool _isSubmitting = false;
  final String _apiUrl =
      'https://mini-crm-production-4f5f.up.railway.app/users';

  //////////////////////////////////////////////////////////////////////////////
  /// Private functions

  Future<void> _selectBirthDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedBirthDate ?? DateTime(2000),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(), // não pode ser no futuro
    );
    if (picked != null && picked != _selectedBirthDate) {
      setState(() {
        _selectedBirthDate = picked;
        _birthDateCtrl.text = DateFormat('dd/MM/yyyy', 'pt_BR').format(picked);
      });
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isSubmitting = true);

    final String? formattedBirthDate = _selectedBirthDate
        ?.toIso8601String()
        .split('T')
        .first;

    final payload = jsonEncode({
      'client_full_name': _userFullNameCtrl.text,
      'birth_date': formattedBirthDate,
      'email': _emailCtrl.text,
      'telephone': _telephoneCtrl.text.isEmpty ? null : _telephoneCtrl.text,
      'cpf': _cpfCtrl.text,
    });

    try {
      final response = await http.post(
        Uri.parse(_apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: payload,
      );

      if (!mounted) return;

      if (response.statusCode == 201) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Usuário cadastrado com sucesso!')),
        );
        _formKey.currentState!.reset();
        _selectedBirthDate = null;
        _birthDateCtrl.text = '';
      } else {
        // Tenta parsear o detalhe do erro do FastAPI se disponível
        String errorMessage = 'Erro: ${response.statusCode}';
        try {
          final errorBody = jsonDecode(response.body);
          if (errorBody is Map && errorBody.containsKey('detail')) {
            // Se o erro for uma lista de detalhes (Pydantic validation errors)
            if (errorBody['detail'] is List) {
              errorMessage = 'Erros de validação:\n';
              for (var detail in errorBody['detail']) {
                if (detail is Map && detail.containsKey('msg')) {
                  errorMessage += '- ${detail['msg']}\n';
                }
              }
            } else {
              // Se for uma string de detalhe (ex: "User with this email already exists.")
              errorMessage = 'Erro: ${errorBody['detail']}';
            }
          }
        } catch (e) {
          debugPrint('Failed to parse error response: $e');
        }
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(errorMessage)));
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Falha ao enviar: $e')));
    } finally {
      if (mounted) {
        setState(() => _isSubmitting = false);
      }
    }
  }

  //////////////////////////////////////////////////////////////////////////////
  /// Lifecycle methods

  @override
  void dispose() {
    _userFullNameCtrl.dispose();
    _emailCtrl.dispose();
    _telephoneCtrl.dispose();
    _cpfCtrl.dispose();
    _birthDateCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        CustomPaint(
          // Onde o Painter será desenhado
          painter: CurvedBackgroundPainter(
            color1: kcDarkGreen,
            color2: kcLightPink,
          ),
          child: Container(),
        ),
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Form(
            key: _formKey,
            child: ListView(
              children: [
                const SizedBox(height: 4),
                TextFormField(
                  controller: _userFullNameCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Nome Completo do Cliente',
                  ),
                  validator: (v) => v == null || v.isEmpty || v.length < 3
                      ? 'Nome completo deve ter pelo menos 3 caracteres'
                      : null,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _birthDateCtrl,
                  decoration: InputDecoration(
                    labelText: 'Data de Nascimento (DD/MM/YYYY)',
                    suffixIcon: IconButton(
                      icon: const Icon(Icons.calendar_today),
                      onPressed: () => _selectBirthDate(context),
                    ),
                  ),
                  readOnly: true, // Impede que o usuário digite a data
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Campo obrigatório' : null,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _emailCtrl,
                  decoration: const InputDecoration(labelText: 'Email'),
                  keyboardType: TextInputType.emailAddress,
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Campo obrigatório';
                    final regex = RegExp(r"^[^@\s]+@[^@\s]+\.[^@\s]+$");
                    if (!regex.hasMatch(v)) return 'Email inválido';
                    return null;
                  },
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _telephoneCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Telefone (Ex: +5511987654321 ou 912341234)',
                  ),
                  keyboardType: TextInputType.phone,
                  validator: (v) {
                    if (v != null && v.isNotEmpty) {
                      final regex = RegExp(
                        r"^\+?\d{9,14}$",
                      ); // O mesmo regex do backend
                      if (!regex.hasMatch(v)) {
                        return 'Telefone inválido (Ex: +5511987654321 ou 912341234)';
                      }
                    }
                    return null; // Opcional no backend, então pode ser nulo aqui
                  },
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _cpfCtrl,
                  decoration: const InputDecoration(
                    labelText: 'CPF (apenas números)',
                  ),
                  keyboardType: TextInputType.number,
                  maxLength: 11, // Limita a 11 dígitos
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Campo obrigatório';
                    final regex = RegExp(
                      r"^\d{11}$",
                    ); // O mesmo regex do backend
                    if (!regex.hasMatch(v)) {
                      return 'CPF inválido (apenas 11 números)';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 24), // Espaço antes do botão
                ElevatedButton(
                  onPressed: _isSubmitting ? null : _submit,
                  style: ElevatedButton.styleFrom(backgroundColor: kcDarkGreen),
                  child: _isSubmitting
                      ? const SizedBox(
                          height: 24,
                          width: 24,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text(
                          'Cadastrar Usuário',
                          style: TextStyle(color: kcLightPink),
                        ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class CurvedBackgroundPainter extends CustomPainter {
  final Color color1;
  final Color color2;

  CurvedBackgroundPainter({required this.color1, required this.color2});

  @override
  void paint(Canvas canvas, Size size) {
    final Path path1 = Path();
    final Path path2 = Path();

    // Desenha a primeira curva (verde escuro)
    path1.moveTo(0, size.height * 0.7); // Começa na metade inferior esquerda
    path1.quadraticBezierTo(
      size.width * 0.25,
      size.height * 0.6, // Ponto de controle 1
      size.width * 0.5,
      size.height * 0.8, // Ponto final 1
    );
    path1.quadraticBezierTo(
      size.width * 0.75,
      size.height * 0.9, // Ponto de controle 2
      size.width,
      size.height * 0.7, // Ponto final 2
    );
    path1.lineTo(
      size.width,
      size.height,
    ); // Desce para o canto inferior direito
    path1.lineTo(0, size.height); // Vai para o canto inferior esquerdo
    path1.close(); // Fecha o caminho
    canvas.drawPath(path1, Paint()..color = color1);

    // Desenha a segunda curva (rosa claro/bege)
    path2.moveTo(0, size.height * 0.8); // Começa um pouco mais abaixo
    path2.quadraticBezierTo(
      size.width * 0.3,
      size.height * 0.9, // Ponto de controle 1
      size.width * 0.7,
      size.height * 0.75, // Ponto final 1
    );
    path2.quadraticBezierTo(
      size.width * 0.9,
      size.height * 0.65, // Ponto de controle 2
      size.width,
      size.height * 0.85, // Ponto final 2
    );
    path2.lineTo(size.width, size.height);
    path2.lineTo(0, size.height);
    path2.close();
    canvas.drawPath(path2, Paint()..color = color2);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false; // Não precisa redesenhar, pois as cores são fixas
  }
}
