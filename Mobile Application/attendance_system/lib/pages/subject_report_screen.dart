import 'package:flutter/material.dart';
import '../widgets/common_app_bar.dart';
import '../widgets/sub_header_bar.dart' as subheader;
import '../services/enrollment_service.dart';
import '../services/attendance_service.dart';
import '../widgets/bottom_nav_bar.dart';

class SubjectReportScreen extends StatefulWidget {
  final String subject;
  const SubjectReportScreen({super.key, required this.subject});

  @override
  State<SubjectReportScreen> createState() => _SubjectReportScreenState();
}

class _SubjectReportScreenState extends State<SubjectReportScreen> {
  late String selectedSubject;
  List<String> subjects = [];
  List<List<String>> attendanceRows = [];
  bool _loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    selectedSubject = widget.subject;
    _loadSubjectsAndAttendance();
  }

  Future<void> _loadSubjectsAndAttendance() async {
    try {
      subjects = await EnrollmentService().fetchStudentSubjects();
      await _loadAttendance();
    } catch (e) {
      setState(() {
        error = e.toString();
        _loading = false;
      });
    }
  }

  Future<void> _loadAttendance() async {
    try {
      setState(() {
        _loading = true;
        error = null;
      });

      final data = await AttendanceService().fetchAttendanceBySubject(
        selectedSubject,
      );
      setState(() {
        attendanceRows = data;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        error = e.toString();
        _loading = false;
      });
    }
  }

  TableRow _buildHeaderRow() {
    return const TableRow(
      decoration: BoxDecoration(color: Color(0xFFEDEDED)),
      children: [
        Padding(padding: EdgeInsets.all(8), child: Text('Date')),
        Padding(padding: EdgeInsets.all(8), child: Text('Session')),
        Padding(padding: EdgeInsets.all(8), child: Text('Status')),
        Padding(padding: EdgeInsets.all(8), child: Text('Remarks')),
      ],
    );
  }

  List<TableRow> _getRows() {
    return attendanceRows.map((entry) {
      final icon = _buildStatusIcon(entry[2]);
      return TableRow(
        children: [
          _buildTableCell(entry[0]),
          _buildTableCell(entry[1]),
          Padding(
            padding: const EdgeInsets.all(8),
            child: Row(
              children: [
                icon,
                const SizedBox(width: 4),
                Flexible(
                  child: Text(entry[2], overflow: TextOverflow.ellipsis),
                ),
              ],
            ),
          ),
          _buildTableCell(entry[3]),
        ],
      );
    }).toList();
  }

  Widget _buildTableCell(String text) {
    return Padding(
      padding: const EdgeInsets.all(8),
      child: Text(text, overflow: TextOverflow.ellipsis),
    );
  }

  Widget _buildStatusIcon(String status) {
    if (status == 'present')
      return const Icon(Icons.check, color: Colors.green, size: 18);
    if (status == 'absent')
      return const Icon(Icons.close, color: Colors.red, size: 18);
    return const Icon(Icons.access_time, color: Colors.orange, size: 18);
  }

  @override
  Widget build(BuildContext context) {
    int presentCount = attendanceRows.where((e) => e[2] == 'present').length;
    double percent = attendanceRows.isEmpty
        ? 0
        : (presentCount / attendanceRows.length);
    int percentage = (percent * 100).round();

    return Scaffold(
      appBar: const CommonAppBar(title: 'Attendance System'),
      bottomNavigationBar: const BottomNavBar(currentIndex: 0),
      body: SafeArea(
        child: Column(
          children: [
            subheader.SubHeaderBar(
              title: 'Report',
              onBack: () => Navigator.pop(context),
              trailing: DropdownButton<String>(
                value: selectedSubject,
                underline: const SizedBox(),
                items: subjects
                    .map(
                      (s) => DropdownMenuItem(
                        value: s,
                        child: Text(s, style: const TextStyle(fontSize: 14)),
                      ),
                    )
                    .toList(),
                onChanged: (value) {
                  if (value != null && value != selectedSubject) {
                    setState(() {
                      selectedSubject = value;
                      _loading = true;
                    });
                    _loadAttendance();
                  }
                },
              ),
            ),
            if (_loading)
              const Expanded(child: Center(child: CircularProgressIndicator()))
            else if (error != null)
              Expanded(
                child: Center(
                  child: Text(error!, style: TextStyle(color: Colors.red)),
                ),
              )
            else
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Attendance Overview',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Stack(
                        alignment: Alignment.centerLeft,
                        children: [
                          Container(
                            height: 20,
                            decoration: BoxDecoration(
                              color: Colors.grey[300],
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                          Container(
                            height: 20,
                            width: MediaQuery.of(context).size.width * percent,
                            decoration: BoxDecoration(
                              color: Colors.green,
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                          Positioned(
                            left: 10,
                            child: Text(
                              '$percentage%',
                              style: const TextStyle(color: Colors.white),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      Text('Total Sessions: ${attendanceRows.length}'),
                      Text('Attended: $presentCount'),
                      Text(
                        'Late: ${attendanceRows.where((e) => e[2] == 'pending').length}',
                      ),
                      Text('Percentage: $percentage%'),
                      const SizedBox(height: 20),
                      const Divider(),
                      const Text(
                        'Detailed List',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Container(
                        constraints: const BoxConstraints(maxHeight: 280),
                        child: SingleChildScrollView(
                          child: Table(
                            columnWidths: const {
                              0: FlexColumnWidth(2),
                              1: FlexColumnWidth(3),
                              2: FlexColumnWidth(2),
                              3: FlexColumnWidth(4),
                            },
                            border: TableBorder.all(color: Colors.black12),
                            children: [_buildHeaderRow(), ..._getRows()],
                          ),
                        ),
                      ),
                      const SizedBox(height: 10),
                    ],
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
