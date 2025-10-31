# Flutter API Extended Reference

This document provides additional Flutter API references and advanced patterns beyond the main SKILL.md guide.

## Advanced Widget Patterns

### Slivers for Custom Scrolling

Slivers are low-level scrollable components that allow for more complex scrolling effects.

```dart
CustomScrollView(
  slivers: [
    // App bar that collapses when scrolling
    SliverAppBar(
      expandedHeight: 200.0,
      floating: false,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: Text('Collapsing App Bar'),
        background: Image.network('url', fit: BoxFit.cover),
      ),
    ),

    // Grid section
    SliverGrid(
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
      ),
      delegate: SliverChildBuilderDelegate(
        (context, index) => Card(child: Center(child: Text('Item $index'))),
        childCount: 20,
      ),
    ),

    // List section
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ListTile(title: Text('List Item $index')),
        childCount: 50,
      ),
    ),

    // Fixed box
    SliverToBoxAdapter(
      child: Container(
        height: 100,
        color: Colors.blue,
        child: Center(child: Text('Fixed Content')),
      ),
    ),

    // Persistent header
    SliverPersistentHeader(
      pinned: true,
      delegate: MySliverPersistentHeaderDelegate(),
    ),
  ],
)
```

### Custom Paint for Drawing

```dart
class MyPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blue
      ..strokeWidth = 4
      ..style = PaintingStyle.stroke;

    // Draw circle
    canvas.drawCircle(
      Offset(size.width / 2, size.height / 2),
      50,
      paint,
    );

    // Draw line
    canvas.drawLine(
      Offset(0, 0),
      Offset(size.width, size.height),
      paint,
    );

    // Draw path
    final path = Path()
      ..moveTo(0, size.height / 2)
      ..quadraticBezierTo(
        size.width / 2, 0,
        size.width, size.height / 2,
      );
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

// Usage
CustomPaint(
  size: Size(200, 200),
  painter: MyPainter(),
)
```

## State Management Libraries

### Provider Pattern

```dart
// Install: flutter pub add provider

// 1. Create a ChangeNotifier
class CounterProvider extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }

  void decrement() {
    _count--;
    notifyListeners();
  }
}

// 2. Provide it at the top level
ChangeNotifierProvider(
  create: (_) => CounterProvider(),
  child: MyApp(),
)

// 3. Consume in widgets
Consumer<CounterProvider>(
  builder: (context, counter, child) {
    return Text('Count: ${counter.count}');
  },
)

// Or use Provider.of
final counter = Provider.of<CounterProvider>(context);

// Or use context.watch (shorthand)
final counter = context.watch<CounterProvider>();
context.read<CounterProvider>().increment(); // Don't trigger rebuild
```

### Riverpod (Recommended Modern Approach)

```dart
// Install: flutter pub add flutter_riverpod

// 1. Define providers
final counterProvider = StateProvider<int>((ref) => 0);

final userProvider = FutureProvider<User>((ref) async {
  return fetchUser();
});

// 2. Wrap app
ProviderScope(
  child: MyApp(),
)

// 3. Use ConsumerWidget
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);

    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => ref.read(counterProvider.notifier).state++,
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

### BLoC Pattern

```dart
// Install: flutter pub add flutter_bloc

// 1. Define events
abstract class CounterEvent {}
class Increment extends CounterEvent {}
class Decrement extends CounterEvent {}

// 2. Define states
class CounterState {
  final int count;
  CounterState(this.count);
}

// 3. Create BLoC
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(CounterState(0)) {
    on<Increment>((event, emit) => emit(CounterState(state.count + 1)));
    on<Decrement>((event, emit) => emit(CounterState(state.count - 1)));
  }
}

// 4. Provide BLoC
BlocProvider(
  create: (_) => CounterBloc(),
  child: MyApp(),
)

// 5. Use BlocBuilder
BlocBuilder<CounterBloc, CounterState>(
  builder: (context, state) {
    return Text('Count: ${state.count}');
  },
)

// 6. Dispatch events
context.read<CounterBloc>().add(Increment());
```

## Network & HTTP

### Using http package

```dart
// Install: flutter pub add http

import 'package:http/http.dart' as http;
import 'dart:convert';

// GET request
Future<List<Post>> fetchPosts() async {
  final response = await http.get(
    Uri.parse('https://jsonplaceholder.typicode.com/posts'),
  );

  if (response.statusCode == 200) {
    final List<dynamic> data = json.decode(response.body);
    return data.map((json) => Post.fromJson(json)).toList();
  } else {
    throw Exception('Failed to load posts');
  }
}

// POST request
Future<Post> createPost(Post post) async {
  final response = await http.post(
    Uri.parse('https://jsonplaceholder.typicode.com/posts'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode(post.toJson()),
  );

  if (response.statusCode == 201) {
    return Post.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to create post');
  }
}

// Model class
class Post {
  final int id;
  final String title;
  final String body;

  Post({required this.id, required this.title, required this.body});

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'],
      title: json['title'],
      body: json['body'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'body': body,
    };
  }
}
```

### Using Dio (Advanced HTTP Client)

```dart
// Install: flutter pub add dio

import 'package:dio/dio.dart';

final dio = Dio(
  BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: Duration(seconds: 5),
    receiveTimeout: Duration(seconds: 3),
    headers: {'Authorization': 'Bearer token'},
  ),
);

// Interceptors for logging/auth
dio.interceptors.add(
  InterceptorsWrapper(
    onRequest: (options, handler) {
      print('Request: ${options.method} ${options.path}');
      return handler.next(options);
    },
    onResponse: (response, handler) {
      print('Response: ${response.statusCode}');
      return handler.next(response);
    },
    onError: (error, handler) {
      print('Error: ${error.message}');
      return handler.next(error);
    },
  ),
);

// Usage
Future<List<User>> fetchUsers() async {
  try {
    final response = await dio.get('/users');
    return (response.data as List)
        .map((json) => User.fromJson(json))
        .toList();
  } on DioException catch (e) {
    throw Exception('Network error: ${e.message}');
  }
}
```

## Local Storage

### Shared Preferences

```dart
// Install: flutter pub add shared_preferences

import 'package:shared_preferences/shared_preferences.dart';

// Save data
Future<void> saveUserData(String name, int age) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('name', name);
  await prefs.setInt('age', age);
  await prefs.setBool('isLoggedIn', true);
  await prefs.setStringList('favorites', ['item1', 'item2']);
}

// Read data
Future<String?> getUserName() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString('name');
}

// Remove data
Future<void> clearUserData() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.remove('name');
  // or clear all
  await prefs.clear();
}
```

### SQLite Database

```dart
// Install: flutter pub add sqflite path

import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'app_database.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER
          )
        ''');
      },
    );
  }

  Future<int> insertUser(Map<String, dynamic> user) async {
    final db = await database;
    return await db.insert('users', user);
  }

  Future<List<Map<String, dynamic>>> getUsers() async {
    final db = await database;
    return await db.query('users');
  }

  Future<int> updateUser(int id, Map<String, dynamic> user) async {
    final db = await database;
    return await db.update('users', user, where: 'id = ?', whereArgs: [id]);
  }

  Future<int> deleteUser(int id) async {
    final db = await database;
    return await db.delete('users', where: 'id = ?', whereArgs: [id]);
  }
}
```

## Firebase Integration

```dart
// Install Firebase packages:
// flutter pub add firebase_core firebase_auth cloud_firestore

// 1. Initialize Firebase (in main.dart)
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}

// 2. Authentication
class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  // Sign up
  Future<UserCredential> signUp(String email, String password) async {
    return await _auth.createUserWithEmailAndPassword(
      email: email,
      password: password,
    );
  }

  // Sign in
  Future<UserCredential> signIn(String email, String password) async {
    return await _auth.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
  }

  // Sign out
  Future<void> signOut() async {
    await _auth.signOut();
  }

  // Current user stream
  Stream<User?> get authStateChanges => _auth.authStateChanges();
}

// 3. Firestore
class FirestoreService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  // Add document
  Future<void> addUser(String id, Map<String, dynamic> data) async {
    await _db.collection('users').doc(id).set(data);
  }

  // Get document
  Future<DocumentSnapshot> getUser(String id) async {
    return await _db.collection('users').doc(id).get();
  }

  // Stream of documents
  Stream<QuerySnapshot> getUsersStream() {
    return _db.collection('users').snapshots();
  }

  // Query
  Future<List<QueryDocumentSnapshot>> getUsersByAge(int minAge) async {
    final snapshot = await _db
        .collection('users')
        .where('age', isGreaterThan: minAge)
        .orderBy('age')
        .limit(10)
        .get();
    return snapshot.docs;
  }

  // Update
  Future<void> updateUser(String id, Map<String, dynamic> data) async {
    await _db.collection('users').doc(id).update(data);
  }

  // Delete
  Future<void> deleteUser(String id) async {
    await _db.collection('users').doc(id).delete();
  }
}
```

## Testing

### Widget Testing

```dart
// In test/widget_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:myapp/main.dart';

void main() {
  testWidgets('Counter increments', (WidgetTester tester) async {
    // Build widget
    await tester.pumpWidget(MyApp());

    // Verify initial state
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // Tap button
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // Verify updated state
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });

  testWidgets('TextField input', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: MyForm()));

    // Find text field
    final textField = find.byType(TextField);

    // Enter text
    await tester.enterText(textField, 'Hello');
    await tester.pump();

    // Verify
    expect(find.text('Hello'), findsOneWidget);
  });
}
```

### Unit Testing

```dart
// In test/unit_test.dart
import 'package:test/test.dart';

void main() {
  group('Calculator', () {
    test('addition', () {
      expect(2 + 2, equals(4));
    });

    test('subtraction', () {
      expect(5 - 3, equals(2));
    });
  });

  group('User', () {
    late User user;

    setUp(() {
      user = User(name: 'John', age: 25);
    });

    test('user creation', () {
      expect(user.name, equals('John'));
      expect(user.age, equals(25));
    });

    test('user validation', () {
      expect(user.isAdult(), isTrue);
    });
  });
}
```

## Additional Resources

### Official Documentation
- Flutter API Reference: https://api.flutter.dev/
- Flutter Docs: https://docs.flutter.dev/
- Dart Language Tour: https://dart.dev/guides/language/language-tour
- Widget Catalog: https://docs.flutter.dev/ui/widgets
- Cookbook: https://docs.flutter.dev/cookbook

### Package Resources
- Pub.dev: https://pub.dev/ (Official package repository)
- Provider: https://pub.dev/packages/provider
- Riverpod: https://riverpod.dev/
- BLoC: https://bloclibrary.dev/
- Dio: https://pub.dev/packages/dio
- Firebase: https://firebase.flutter.dev/

### Learning Resources
- Flutter Codelabs: https://docs.flutter.dev/codelabs
- Flutter YouTube Channel: https://www.youtube.com/c/flutterdev
- Flutter Community: https://flutter.dev/community
