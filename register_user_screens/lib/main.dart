import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'form_page.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Formulário para Registro de Usuários',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            minimumSize: const Size(double.infinity, 48),
            textStyle: const TextStyle(fontSize: 16),
          ),
        ),
      ),
      home: Scaffold(
        appBar: AppBar(title: Center(child: Text('Cadastro de usuário'))),
        body: Column(
          children: [
            Image.asset('lib/assets/banner_a.png', height: 80),
            Expanded(child: FormPage()),
          ],
        ),
      ),

      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        // GlobalCupertinoLocalizations.delegate
      ],
      supportedLocales: const [Locale('pt', 'BR')],
    );
  }
}
