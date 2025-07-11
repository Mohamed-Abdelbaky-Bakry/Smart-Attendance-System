import 'package:flutter/material.dart';
import '../services/notification_service.dart';
import '../widgets/common_app_bar.dart';
import '../widgets/sub_header_bar.dart' as header;
import '../widgets/bottom_nav_bar.dart';

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({super.key});

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  final svc = NotificationService(
    baseUrl: 'http://10.0.2.2:8000',
    // headers: {'Authorization': 'Bearer YOUR_TOKEN'},
  );
  List<Map<String, String>> notifications = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchNotifs();
  }

  Future<void> fetchNotifs() async {
    final list = await svc.fetchStudentNotifications();
    if (!mounted) return;
    setState(() {
      notifications = list;
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CommonAppBar(title: 'Attendance System'),
      bottomNavigationBar: const BottomNavBar(currentIndex: 1),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          header.SubHeaderBar(
            title: 'Notifications',
            onBack: () => Navigator.pop(context),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            child: Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: () {
                  if (!mounted) return;
                  setState(() => notifications.clear());
                },
                child: const Text(
                  'Mark All as Read',
                  style: TextStyle(color: Colors.teal),
                ),
              ),
            ),
          ),
          Expanded(
            child: isLoading
                ? const Center(child: CircularProgressIndicator())
                : notifications.isEmpty
                ? const Center(child: Text('No Notifications'))
                : ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    itemCount: notifications.length,
                    itemBuilder: (c, i) {
                      final n = notifications[i];
                      return NotificationCard(
                        title: n['title']!,
                        subtitle: n['subtitle']!,
                        label: n['label']!,
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}

class NotificationCard extends StatelessWidget {
  final String title, subtitle, label;
  const NotificationCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    final color = label == 'Alert'
        ? Colors.red
        : label == 'Upcoming'
        ? Colors.green
        : label == 'Approved'
        ? Colors.blue
        : Colors.grey;
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: ListTile(
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle),
        trailing: Text(label, style: TextStyle(fontSize: 12, color: color)),
      ),
    );
  }
}
