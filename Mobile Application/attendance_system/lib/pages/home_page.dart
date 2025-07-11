import 'package:flutter/material.dart';
import '../widgets/common_app_bar.dart';
import '../widgets/bottom_nav_bar.dart';
import '../widgets/subject_card.dart';
import '../services/enrollment_service.dart';
import 'subject_report_screen.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<String> subjects = [];
  bool _loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    _fetchSubjects();
  }

  Future<void> _fetchSubjects() async {
    try {
      final data = await EnrollmentService().fetchStudentSubjects();
      setState(() {
        subjects = data;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        error = e.toString();
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CommonAppBar(title: 'Attendance System'),
      bottomNavigationBar: const BottomNavBar(currentIndex: 0),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : error != null
          ? Center(
              child: Text(
                'Error: $error',
                style: const TextStyle(color: Colors.red),
              ),
            )
          : subjects.isEmpty
          ? const Center(child: Text('No subjects found.'))
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: subjects.length,
              itemBuilder: (context, index) {
                return SubjectCard(
                  subjectName: subjects[index],
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            SubjectReportScreen(subject: subjects[index]),
                      ),
                    );
                  },
                );
              },
            ),
    );
  }
}
