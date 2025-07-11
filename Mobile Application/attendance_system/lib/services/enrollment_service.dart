import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class EnrollmentService {
  static const String baseUrl = 'http://10.0.2.2:8000';

  Future<List<String>> fetchStudentSubjects() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');

    if (token == null) throw Exception('Token is missing');

    final response = await http.get(
      Uri.parse('$baseUrl/enrollments/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      final subjects = data
          .map<String>((e) => e['subject']['name'].toString())
          .toSet()
          .toList();
      return subjects;
    } else {
      throw Exception('Failed to load subjects: ${response.body}');
    }
  }
}
