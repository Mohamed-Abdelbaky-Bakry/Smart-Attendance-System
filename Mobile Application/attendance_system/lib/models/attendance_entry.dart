class AttendanceEntry {
  final String id;
  final String subjectId;
  final DateTime date;
  final String session;
  final String status; // Present, Absent, Late
  final String remarks;

  AttendanceEntry({
    required this.id,
    required this.subjectId,
    required this.date,
    required this.session,
    required this.status,
    required this.remarks,
  });
}
