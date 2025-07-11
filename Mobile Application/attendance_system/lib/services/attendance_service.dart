import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class AttendanceService {
  static const String baseUrl = 'http://10.0.2.2:8000';

  Future<List<List<String>>> fetchAttendanceBySubject(
    String subjectName,
  ) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    final email = prefs.getString('email');

    if (token == null || email == null) throw Exception('Missing credentials');

    final response = await http.get(
      Uri.parse('$baseUrl/attendance/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      final filtered = data.where(
        (e) =>
            e['student']['account']['email'] == email &&
            e['session_date']['class_session']['subject']['name'] ==
                subjectName,
      );

      return filtered.map<List<String>>((e) {
        return [
          e['session_date']['session_date'].toString(),
          'Session ${e['session_date']['class_session']['period_index']}',
          e['status'].toString(),
          e['remarks']?.toString() ?? '',
        ];
      }).toList();
    } else {
      throw Exception('Failed to load attendance: ${response.body}');
    }
  }
}
