import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SubjectService {
  static const _baseUrl =
      'http://10.0.2.2:8000'; // IP للمحاكي أو عدله حسب السيرفر

  final _storage = const FlutterSecureStorage();

  Future<List<Subject>> fetchSubjects() async {
    final token = await _storage.read(key: 'token');

    if (token == null) {
      throw Exception('Authentication token not found');
    }

    final response = await http.get(
      Uri.parse('$_baseUrl/student/subjects/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Subject.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load subjects: ${response.body}');
    }
  }
}

class Subject {
  final int id;
  final String name;
  final String code;

  Subject({required this.id, required this.name, required this.code});

  factory Subject.fromJson(Map<String, dynamic> json) {
    return Subject(id: json['id'], name: json['name'], code: json['code']);
  }
}
