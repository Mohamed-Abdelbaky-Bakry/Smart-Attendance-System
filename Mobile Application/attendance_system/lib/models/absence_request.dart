enum AbsenceStatus { pending, approved, rejected }

class AbsenceRequest {
  final String id;
  final String userId;
  final String subjectId;
  final DateTime startDate;
  final DateTime endDate;
  final String reason;
  final AbsenceStatus status;
  final String adminRemarks;

  AbsenceRequest({
    required this.id,
    required this.userId,
    required this.subjectId,
    required this.startDate,
    required this.endDate,
    required this.reason,
    this.status = AbsenceStatus.pending,
    this.adminRemarks = '',
  });
}
