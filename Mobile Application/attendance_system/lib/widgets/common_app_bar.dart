import 'package:flutter/material.dart';

/// Top AppBar used on all screens
class CommonAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;

  const CommonAppBar({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return AppBar(
      automaticallyImplyLeading: false, // No default back arrow
      title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
      centerTitle: true,
      backgroundColor: const Color(0xFF2F897D),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(56.0);
}

/// Section below AppBar with optional back arrow and dropdown
class SubHeaderBar extends StatelessWidget {
  final String title;
  final VoidCallback? onBack;
  final Widget? trailing;

  const SubHeaderBar({
    super.key,
    required this.title,
    this.onBack,
    this.trailing,
  });

  @override
  Widget build(BuildContext context) {
    final bool showBack = onBack != null;

    return Container(
      height: 48,
      color: Colors.grey.shade100,
      padding: const EdgeInsets.symmetric(horizontal: 10),
      child: Row(
        mainAxisAlignment: showBack
            ? MainAxisAlignment.start
            : MainAxisAlignment.center,
        children: [
          if (showBack)
            IconButton(icon: const Icon(Icons.arrow_back), onPressed: onBack),
          if (!showBack)
            Expanded(
              child: Center(
                child: Text(
                  title,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            )
          else
            Text(
              title,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          if (trailing != null) ...[const Spacer(), trailing!],
        ],
      ),
    );
  }
}
