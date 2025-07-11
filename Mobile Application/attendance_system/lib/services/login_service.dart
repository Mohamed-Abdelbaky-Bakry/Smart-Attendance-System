import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  static const String baseUrl = 'http://10.0.2.2:8000';

  Future<Map<String, dynamic>> login(String email, String password) async {
    final url = Uri.parse('$baseUrl/accounts/login/');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      final body = jsonDecode(response.body);
      final accessToken = body['access'];
      final refreshToken = body['refresh'];

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', accessToken);
      await prefs.setString('refresh', refreshToken);
      await prefs.setString('email', email);

      // Get user data from /students/
      final studentUrl = Uri.parse('$baseUrl/students/');
      final studentRes = await http.get(
        studentUrl,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $accessToken',
        },
      );

      if (studentRes.statusCode == 200) {
        final List students = jsonDecode(studentRes.body);
        final student = students.firstWhere(
          (s) => s['account']['email'] == email,
          orElse: () => null,
        );

        if (student != null) {
          final userData = {
            'email': student['account']['email'],
            'name': student['account']['name'],
          };
          await prefs.setString('user', jsonEncode(userData));
        }
      }

      return {'success': true, 'token': accessToken};
    } else {
      final body = jsonDecode(response.body);
      return {
        'success': false,
        'message': body['detail'] ?? 'Login failed: unknown error',
      };
    }
  }
}
