import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../widgets/bottom_nav_bar.dart';

class RequestListScreen extends StatefulWidget {
  const RequestListScreen({super.key});
  @override
  State<RequestListScreen> createState() => _RequestListScreenState();
}

class _RequestListScreenState extends State<RequestListScreen> {
  List<Map<String, dynamic>> requests = [];
  bool isLoading = true;
  String? selectedSubject;
  final _reasonCtrl = TextEditingController();
  List<Map<String, dynamic>> subjects = [];

  @override
  void initState() {
    super.initState();
    _loadSubjects();
    _loadRequests();
  }

  Future<void> _loadSubjects() async {
    final token = await SharedPreferences.getInstance().then(
      (p) => p.getString('token'),
    );
    final res = await http.get(
      Uri.parse('http://10.0.2.2:8000/subjects/'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      setState(() {
        subjects = (data as List)
            .map((e) => {'id': e['id'], 'name': e['name']})
            .toList();
      });
    }
  }

  Future<void> _loadRequests() async {
    setState(() => isLoading = true);
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    final res = await http.get(
      Uri.parse('http://10.0.2.2:8000/requests/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );
    if (!mounted) return;
    if (res.statusCode == 200) {
      final data = json.decode(utf8.decode(res.bodyBytes)) as List;
      setState(() {
        requests = data
            .map(
              (item) => {
                'subject': item['subject']['name'],
                'type': item['request_type'],
                'status': item['status'],
                'submitted': item['created_at'],
                'replied_at': item['replied_at'] ?? '',
                'comment': item['instructor_comment'] ?? '',
              },
            )
            .toList();
      });
    }
    setState(() => isLoading = false);
  }

  Future<void> _openNewRequestForm() async {
    setState(() {
      _reasonCtrl.clear();
      selectedSubject = subjects.isEmpty
          ? null
          : subjects.first['id'].toString();
    });
    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (_) {
        return Padding(
          padding: EdgeInsets.only(
            bottom: MediaQuery.of(context).viewInsets.bottom,
            top: 16,
            left: 16,
            right: 16,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              DropdownButtonFormField<String>(
                value: selectedSubject,
                items: subjects.map((subj) {
                  final id = subj['id'].toString();
                  return DropdownMenuItem(value: id, child: Text(subj['name']));
                }).toList(),
                onChanged: (v) => setState(() => selectedSubject = v),
                decoration: InputDecoration(labelText: 'Subject'),
              ),
              TextField(
                controller: _reasonCtrl,
                decoration: InputDecoration(labelText: 'Reason'),
              ),
              const SizedBox(height: 12),
              ElevatedButton(
                onPressed: _submitNewRequest,
                child: Text('Submit'),
              ),
              const SizedBox(height: 20),
            ],
          ),
        );
      },
    );
  }

  Future<void> _submitNewRequest() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    final res = await http.post(
      Uri.parse('http://10.0.2.2:8000/requests/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'subject': int.parse(selectedSubject!),
        'request_type': 'absence',
        'description': _reasonCtrl.text.trim(),
      }),
    );
    if (res.statusCode == 201) {
      Navigator.pop(context);
      _loadRequests();
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to submit')));
    }
  }

  Color _getCardColor(String status) {
    switch (status) {
      case 'approved':
        return Colors.green[100]!;
      case 'rejected':
        return Colors.red[100]!;
      case 'pending':
        return Colors.yellow[100]!;
      default:
        return Colors.grey[300]!;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('My Requests')),
      bottomNavigationBar: const BottomNavBar(currentIndex: 2),
      floatingActionButton: FloatingActionButton(
        onPressed: _openNewRequestForm,
        child: const Icon(Icons.add),
      ),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : requests.isEmpty
          ? Center(child: Text('No requests yet'))
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: requests.length,
              itemBuilder: (ctx, i) {
                final r = requests[i];
                return Container(
                  margin: const EdgeInsets.symmetric(vertical: 8),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: _getCardColor(r['status']),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Subject: ${r['subject']}'),
                      Text('Type: ${r['type']}'),
                      Text('Status: ${r['status']}'),
                      Text('Submitted: ${r['submitted']}'),
                      if (r['replied_at'].toString().isNotEmpty)
                        Text('Replied at: ${r['replied_at']}'),
                      if (r['comment'].toString().isNotEmpty)
                        Text('Instructor: ${r['comment']}'),
                    ],
                  ),
                );
              },
            ),
    );
  }
}
