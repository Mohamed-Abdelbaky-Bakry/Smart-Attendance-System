import 'package:http/http.dart' as http;
import 'dart:convert';

class NotificationService {
  final String baseUrl;
  final Map<String, String>? headers;

  NotificationService({required this.baseUrl, this.headers});

  Future<List<Map<String, String>>> fetchStudentNotifications() async {
    final now = DateTime.now();
    final respAttend = await http.get(
      Uri.parse('$baseUrl/attendance/'),
      headers: headers,
    );
    final respReq = await http.get(
      Uri.parse('$baseUrl/requests/'),
      headers: headers,
    );

    final List<Map<String, String>> notifs = [];

    if (respAttend.statusCode == 200) {
      final data = json.decode(utf8.decode(respAttend.bodyBytes)) as List;
      final upcoming = data.where((item) {
        final date = DateTime.parse(item['session_date']['session_date']);
        return date.isAfter(now);
      }).toList();

      if (upcoming.isNotEmpty) {
        final next = upcoming.first;
        final dateStr = next['session_date']['session_date'];
        final subj = next['session_date']['class_session']['subject']['name'];
        final loc = next['session_date']['class_session']['location'];

        notifs.add({
          'title': 'Next Lecture: $subj',
          'subtitle': 'On $dateStr at room $loc',
          'label': 'Upcoming',
        });

        if (next['status'] == 'pending') {
          notifs.add({
            'title': 'Missed Check-in',
            'subtitle': 'You haven’t checked in for $subj on $dateStr',
            'label': 'Alert',
          });
        }
      }
    }

    if (respReq.statusCode == 200) {
      final List requests = json.decode(utf8.decode(respReq.bodyBytes));
      for (var req in requests) {
        final status = req['status'];
        final date =
            req['resolved_at']?.split('T').first ??
            req['created_at']?.split('T').first;
        if (status == 'approved' || status == 'rejected') {
          notifs.add({
            'title': status == 'approved'
                ? 'Request Approved'
                : 'Request Rejected',
            'subtitle': '$status on $date',
            'label': status == 'approved' ? 'Approved' : 'Rejected',
          });
        }
      }
    }

    return notifs;
  }
}
