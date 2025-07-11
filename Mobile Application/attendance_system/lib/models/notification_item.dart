class NotificationItem {
  final String id;
  final String userId;
  final String title;
  final String description;
  final DateTime date;
  final bool isRead;

  NotificationItem({
    required this.id,
    required this.userId,
    required this.title,
    required this.description,
    required this.date,
    this.isRead = false,
  });
}
