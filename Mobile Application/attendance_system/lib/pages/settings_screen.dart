import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../widgets/bottom_nav_bar.dart';
import '../widgets/common_app_bar.dart' as common;
import '../widgets/sub_header_bar.dart' as subheader;
import '../pages/profile_screen.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool notificationsEnabled = true;
  String selectedLanguage = 'English';
  String userName = 'Loading...';
  String userEmail = '';
  final List<String> languages = ['English', 'Arabic', 'French'];

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  Future<void> _loadUserData() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonData = prefs.getString('user');
    if (jsonData != null) {
      try {
        final Map<String, dynamic> data = json.decode(jsonData);
        if (!mounted) return;
        setState(() {
          userName = data['name'] ?? data['username'] ?? 'No Name';
          userEmail = data['email'] ?? 'No Email';
        });
      } catch (e) {
        if (!mounted) return;
        setState(() {
          userName = 'Invalid Data';
          userEmail = '';
        });
      }
    } else {
      if (!mounted) return;
      setState(() {
        userName = 'No Data';
        userEmail = 'No Email';
      });
    }
  }

  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    if (!mounted) return;
    Navigator.of(context).pushNamedAndRemoveUntil('/login', (route) => false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const common.CommonAppBar(title: 'Attendance System'),
      bottomNavigationBar: const BottomNavBar(currentIndex: 2),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          subheader.SubHeaderBar(
            title: 'Settings',
            onBack: () => Navigator.pop(context),
          ),
          Expanded(
            child: ListView(
              children: [
                const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  child: Text(
                    'Account',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
                ListTile(
                  leading: const CircleAvatar(
                    backgroundColor: Colors.teal,
                    child: Icon(Icons.person, color: Colors.white),
                  ),
                  title: Text(userName),
                  subtitle: Text(userEmail),
                  trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const ProfileScreen()),
                    );
                  },
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.lock),
                  title: const Text('Change Password'),
                  onTap: () {},
                ),
                ListTile(
                  leading: const Icon(Icons.language),
                  title: const Text('Language'),
                  trailing: DropdownButton<String>(
                    value: selectedLanguage,
                    underline: const SizedBox(),
                    items: languages.map((lang) {
                      return DropdownMenuItem<String>(
                        value: lang,
                        child: Text(lang),
                      );
                    }).toList(),
                    onChanged: (String? newValue) {
                      setState(() {
                        selectedLanguage = newValue!;
                      });
                    },
                  ),
                ),
                SwitchListTile(
                  title: const Text('Enable Notifications'),
                  value: notificationsEnabled,
                  onChanged: (bool value) {
                    setState(() {
                      notificationsEnabled = value;
                    });
                  },
                  secondary: const Icon(Icons.notifications_active),
                ),
                const Divider(),
                const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  child: Text(
                    'Support',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
                ListTile(
                  leading: const Icon(Icons.privacy_tip),
                  title: const Text('Privacy Policy'),
                  onTap: () {},
                ),
                ListTile(
                  leading: const Icon(Icons.article_outlined),
                  title: const Text('Terms of Use'),
                  onTap: () {},
                ),
                ListTile(
                  leading: const Icon(Icons.support_agent),
                  title: const Text('Contact Support'),
                  onTap: () {},
                ),
                const Divider(),
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                    onPressed: _logout,
                    icon: const Icon(Icons.logout),
                    label: const Text('Log Out'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
