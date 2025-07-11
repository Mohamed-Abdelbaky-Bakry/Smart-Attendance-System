class Subject {
  final String id;
  final String name;
  final int totalSessions;
  final int attendedSessions;
  final int lateSessions;

  Subject({
    required this.id,
    required this.name,
    required this.totalSessions,
    required this.attendedSessions,
    required this.lateSessions,
  });

  double get attendancePercentage =>
      totalSessions > 0 ? (attendedSessions / totalSessions) * 100 : 0;
}
