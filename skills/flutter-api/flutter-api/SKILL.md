---
name: flutter-api
description: Comprehensive Flutter API reference guide covering widgets, Material Design, Cupertino, animations, gestures, navigation, state management, and platform integration. Use when developing Flutter applications and needing detailed API knowledge for widgets, layout, styling, animations, platform channels, or any Flutter SDK functionality. Essential for building cross-platform mobile, web, and desktop applications with Flutter.
---

# Flutter API Reference Guide

## Overview

This skill provides comprehensive guidance on Flutter's API, covering all major libraries and packages in the Flutter SDK. Flutter is Google's UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase.

## Core Flutter Libraries

### Widgets (flutter/widgets.dart)

The foundational widget library that provides the basic building blocks for Flutter apps.

#### Basic Widgets

```dart
import 'package:flutter/widgets.dart';

// Container - A convenience widget combining common painting, positioning, and sizing
Container(
  padding: EdgeInsets.all(16.0),
  margin: EdgeInsets.symmetric(horizontal: 8.0),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(8.0),
    boxShadow: [BoxShadow(color: Colors.grey, blurRadius: 4.0)],
  ),
  child: Text('Hello Flutter'),
)

// Text - Display text with styling
Text(
  'Hello World',
  style: TextStyle(
    fontSize: 24.0,
    fontWeight: FontWeight.bold,
    color: Colors.blue,
  ),
)

// Row & Column - Layout widgets
Row(
  mainAxisAlignment: MainAxisAlignment.spaceBetween,
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [
    Icon(Icons.star),
    Text('Rating'),
    Text('4.5'),
  ],
)

Column(
  mainAxisAlignment: MainAxisAlignment.center,
  children: [
    Text('Title'),
    Text('Subtitle'),
  ],
)

// Stack - Overlay widgets
Stack(
  children: [
    Container(color: Colors.blue),
    Positioned(
      top: 10,
      left: 10,
      child: Text('Overlay'),
    ),
  ],
)
```

#### Layout Widgets

```dart
// Padding - Add padding around a widget
Padding(
  padding: EdgeInsets.all(16.0),
  child: Text('Padded text'),
)

// Center - Center a widget
Center(child: Text('Centered'))

// Align - Align widget within parent
Align(
  alignment: Alignment.topRight,
  child: Icon(Icons.close),
)

// SizedBox - Fixed size box or spacing
SizedBox(
  width: 100,
  height: 50,
  child: ElevatedButton(
    onPressed: () {},
    child: Text('Button'),
  ),
)

// Flexible & Expanded - Responsive sizing
Row(
  children: [
    Flexible(
      flex: 2,
      child: Container(color: Colors.red),
    ),
    Expanded(
      flex: 3,
      child: Container(color: Colors.blue),
    ),
  ],
)

// Wrap - Flow layout that wraps children
Wrap(
  spacing: 8.0,
  runSpacing: 4.0,
  children: [
    Chip(label: Text('Tag 1')),
    Chip(label: Text('Tag 2')),
    Chip(label: Text('Tag 3')),
  ],
)
```

#### List Widgets

```dart
// ListView - Scrollable list
ListView(
  children: [
    ListTile(title: Text('Item 1')),
    ListTile(title: Text('Item 2')),
    ListTile(title: Text('Item 3')),
  ],
)

// ListView.builder - Efficient for large lists
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(title: Text(items[index]));
  },
)

// ListView.separated - With separators
ListView.separated(
  itemCount: items.length,
  itemBuilder: (context, index) => ListTile(title: Text(items[index])),
  separatorBuilder: (context, index) => Divider(),
)

// GridView - Grid layout
GridView.count(
  crossAxisCount: 2,
  crossAxisSpacing: 10,
  mainAxisSpacing: 10,
  children: [
    Card(child: Center(child: Text('1'))),
    Card(child: Center(child: Text('2'))),
    Card(child: Center(child: Text('3'))),
    Card(child: Center(child: Text('4'))),
  ],
)

// GridView.builder - Efficient grid
GridView.builder(
  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 3,
    crossAxisSpacing: 10,
    mainAxisSpacing: 10,
  ),
  itemCount: items.length,
  itemBuilder: (context, index) {
    return Card(child: Center(child: Text('Item $index')));
  },
)
```

### Material Design (flutter/material.dart)

Flutter's Material Design implementation with widgets following Material Design guidelines.

#### Material Widgets

```dart
import 'package:flutter/material.dart';

// Scaffold - Basic material app structure
Scaffold(
  appBar: AppBar(
    title: Text('My App'),
    actions: [
      IconButton(icon: Icon(Icons.search), onPressed: () {}),
      IconButton(icon: Icon(Icons.more_vert), onPressed: () {}),
    ],
  ),
  body: Center(child: Text('Content')),
  floatingActionButton: FloatingActionButton(
    onPressed: () {},
    child: Icon(Icons.add),
  ),
  drawer: Drawer(
    child: ListView(
      children: [
        DrawerHeader(child: Text('Header')),
        ListTile(title: Text('Item 1')),
        ListTile(title: Text('Item 2')),
      ],
    ),
  ),
  bottomNavigationBar: BottomNavigationBar(
    items: [
      BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
      BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
      BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
    ],
  ),
)

// Card - Material design card
Card(
  elevation: 4.0,
  margin: EdgeInsets.all(8.0),
  child: Padding(
    padding: EdgeInsets.all(16.0),
    child: Column(
      children: [
        Text('Card Title', style: Theme.of(context).textTheme.headlineSmall),
        SizedBox(height: 8),
        Text('Card content goes here'),
      ],
    ),
  ),
)

// Buttons
ElevatedButton(
  onPressed: () {},
  child: Text('Elevated Button'),
)

TextButton(
  onPressed: () {},
  child: Text('Text Button'),
)

OutlinedButton(
  onPressed: () {},
  child: Text('Outlined Button'),
)

IconButton(
  icon: Icon(Icons.favorite),
  onPressed: () {},
)

FloatingActionButton(
  onPressed: () {},
  child: Icon(Icons.add),
)
```

#### Form Widgets

```dart
// TextField - Text input
TextField(
  decoration: InputDecoration(
    labelText: 'Enter your name',
    hintText: 'John Doe',
    prefixIcon: Icon(Icons.person),
    border: OutlineInputBorder(),
  ),
  onChanged: (value) {
    print('Text changed: $value');
  },
)

// Form with validation
final _formKey = GlobalKey<FormState>();

Form(
  key: _formKey,
  child: Column(
    children: [
      TextFormField(
        decoration: InputDecoration(labelText: 'Email'),
        validator: (value) {
          if (value == null || value.isEmpty) {
            return 'Please enter email';
          }
          if (!value.contains('@')) {
            return 'Please enter valid email';
          }
          return null;
        },
      ),
      TextFormField(
        decoration: InputDecoration(labelText: 'Password'),
        obscureText: true,
        validator: (value) {
          if (value == null || value.length < 6) {
            return 'Password must be at least 6 characters';
          }
          return null;
        },
      ),
      ElevatedButton(
        onPressed: () {
          if (_formKey.currentState!.validate()) {
            // Process form
          }
        },
        child: Text('Submit'),
      ),
    ],
  ),
)

// Checkbox
Checkbox(
  value: isChecked,
  onChanged: (bool? value) {
    setState(() {
      isChecked = value ?? false;
    });
  },
)

// Radio buttons
Column(
  children: [
    RadioListTile<String>(
      title: Text('Option 1'),
      value: 'option1',
      groupValue: selectedOption,
      onChanged: (value) {
        setState(() {
          selectedOption = value!;
        });
      },
    ),
    RadioListTile<String>(
      title: Text('Option 2'),
      value: 'option2',
      groupValue: selectedOption,
      onChanged: (value) {
        setState(() {
          selectedOption = value!;
        });
      },
    ),
  ],
)

// Switch
Switch(
  value: isSwitched,
  onChanged: (value) {
    setState(() {
      isSwitched = value;
    });
  },
)

// Slider
Slider(
  value: currentValue,
  min: 0,
  max: 100,
  divisions: 10,
  label: currentValue.round().toString(),
  onChanged: (value) {
    setState(() {
      currentValue = value;
    });
  },
)
```

#### Dialogs & Sheets

```dart
// AlertDialog
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: Text('Confirm Action'),
    content: Text('Are you sure you want to proceed?'),
    actions: [
      TextButton(
        onPressed: () => Navigator.pop(context),
        child: Text('Cancel'),
      ),
      TextButton(
        onPressed: () {
          // Perform action
          Navigator.pop(context);
        },
        child: Text('Confirm'),
      ),
    ],
  ),
)

// SnackBar
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: Text('Action completed'),
    action: SnackBarAction(
      label: 'Undo',
      onPressed: () {
        // Undo action
      },
    ),
    duration: Duration(seconds: 3),
  ),
)

// Bottom Sheet
showModalBottomSheet(
  context: context,
  builder: (context) {
    return Container(
      height: 200,
      child: Column(
        children: [
          ListTile(
            leading: Icon(Icons.share),
            title: Text('Share'),
            onTap: () {},
          ),
          ListTile(
            leading: Icon(Icons.link),
            title: Text('Copy link'),
            onTap: () {},
          ),
        ],
      ),
    );
  },
)

// Date Picker
showDatePicker(
  context: context,
  initialDate: DateTime.now(),
  firstDate: DateTime(2000),
  lastDate: DateTime(2100),
).then((date) {
  if (date != null) {
    print('Selected date: $date');
  }
});

// Time Picker
showTimePicker(
  context: context,
  initialTime: TimeOfDay.now(),
).then((time) {
  if (time != null) {
    print('Selected time: $time');
  }
});
```

### Cupertino (flutter/cupertino.dart)

iOS-style widgets following Apple's Human Interface Guidelines.

```dart
import 'package:flutter/cupertino.dart';

// CupertinoApp - iOS-style app
CupertinoApp(
  home: CupertinoPageScaffold(
    navigationBar: CupertinoNavigationBar(
      middle: Text('iOS App'),
    ),
    child: Center(child: Text('Content')),
  ),
)

// Cupertino Buttons
CupertinoButton(
  child: Text('iOS Button'),
  onPressed: () {},
)

CupertinoButton.filled(
  child: Text('Filled Button'),
  onPressed: () {},
)

// Cupertino Dialog
showCupertinoDialog(
  context: context,
  builder: (context) => CupertinoAlertDialog(
    title: Text('Alert'),
    content: Text('This is an iOS-style alert'),
    actions: [
      CupertinoDialogAction(
        child: Text('Cancel'),
        onPressed: () => Navigator.pop(context),
      ),
      CupertinoDialogAction(
        isDestructiveAction: true,
        child: Text('Delete'),
        onPressed: () {
          // Delete action
          Navigator.pop(context);
        },
      ),
    ],
  ),
)

// Cupertino Picker
CupertinoPicker(
  itemExtent: 32.0,
  onSelectedItemChanged: (index) {
    print('Selected: $index');
  },
  children: [
    Text('Option 1'),
    Text('Option 2'),
    Text('Option 3'),
  ],
)

// Cupertino Sliver Navigation Bar
CupertinoPageScaffold(
  child: CustomScrollView(
    slivers: [
      CupertinoSliverNavigationBar(
        largeTitle: Text('Large Title'),
      ),
      SliverList(
        delegate: SliverChildBuilderDelegate(
          (context, index) => ListTile(title: Text('Item $index')),
          childCount: 50,
        ),
      ),
    ],
  ),
)
```

### Navigation (flutter/material.dart)

```dart
// Basic navigation
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => SecondScreen()),
);

// Pop back
Navigator.pop(context);

// Named routes
MaterialApp(
  initialRoute: '/',
  routes: {
    '/': (context) => HomeScreen(),
    '/details': (context) => DetailsScreen(),
    '/settings': (context) => SettingsScreen(),
  },
);

// Navigate to named route
Navigator.pushNamed(context, '/details');

// Pass arguments
Navigator.pushNamed(
  context,
  '/details',
  arguments: {'id': 123, 'title': 'Item'},
);

// Receive arguments
class DetailsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final args = ModalRoute.of(context)!.settings.arguments as Map;
    return Scaffold(
      appBar: AppBar(title: Text(args['title'])),
      body: Text('ID: ${args['id']}'),
    );
  }
}

// Replace route
Navigator.pushReplacement(
  context,
  MaterialPageRoute(builder: (context) => NewScreen()),
);

// Remove all and push
Navigator.pushAndRemoveUntil(
  context,
  MaterialPageRoute(builder: (context) => HomeScreen()),
  (route) => false,
);

// Return data from screen
// On second screen
Navigator.pop(context, 'Result data');

// On first screen
final result = await Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => SecondScreen()),
);
print('Result: $result');
```

### Animation (flutter/animation.dart)

```dart
import 'package:flutter/animation.dart';

// AnimationController
class AnimatedWidget extends StatefulWidget {
  @override
  _AnimatedWidgetState createState() => _AnimatedWidgetState();
}

class _AnimatedWidgetState extends State<AnimatedWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(seconds: 2),
      vsync: this,
    );

    _animation = Tween<double>(begin: 0, end: 300).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Container(
          width: _animation.value,
          height: _animation.value,
          color: Colors.blue,
        );
      },
    );
  }
}

// Implicit animations
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  width: isExpanded ? 200 : 100,
  height: isExpanded ? 200 : 100,
  color: isExpanded ? Colors.blue : Colors.red,
  curve: Curves.easeInOut,
)

AnimatedOpacity(
  opacity: isVisible ? 1.0 : 0.0,
  duration: Duration(milliseconds: 500),
  child: Container(color: Colors.blue),
)

AnimatedPositioned(
  duration: Duration(milliseconds: 300),
  top: isTop ? 0 : 100,
  left: isLeft ? 0 : 100,
  child: Container(width: 50, height: 50, color: Colors.red),
)

// Hero animation
// On first screen
Hero(
  tag: 'hero-image',
  child: Image.network('url'),
)

// On second screen
Hero(
  tag: 'hero-image',
  child: Image.network('url'),
)

// TweenAnimationBuilder
TweenAnimationBuilder<double>(
  tween: Tween<double>(begin: 0, end: 1),
  duration: Duration(seconds: 1),
  builder: (context, value, child) {
    return Opacity(
      opacity: value,
      child: Transform.scale(
        scale: value,
        child: child,
      ),
    );
  },
  child: Container(width: 100, height: 100, color: Colors.blue),
)
```

### Gestures (flutter/gestures.dart)

```dart
// GestureDetector
GestureDetector(
  onTap: () => print('Tapped'),
  onDoubleTap: () => print('Double tapped'),
  onLongPress: () => print('Long pressed'),
  onPanUpdate: (details) {
    print('Pan: ${details.delta}');
  },
  onScaleUpdate: (details) {
    print('Scale: ${details.scale}');
  },
  child: Container(
    width: 200,
    height: 200,
    color: Colors.blue,
    child: Center(child: Text('Touch me')),
  ),
)

// InkWell - Material ripple effect
InkWell(
  onTap: () {},
  onLongPress: () {},
  splashColor: Colors.blue.withOpacity(0.3),
  child: Container(
    padding: EdgeInsets.all(16),
    child: Text('Tap me'),
  ),
)

// Dismissible - Swipe to dismiss
Dismissible(
  key: Key(item.id),
  direction: DismissDirection.endToStart,
  background: Container(
    color: Colors.red,
    alignment: Alignment.centerRight,
    padding: EdgeInsets.only(right: 16),
    child: Icon(Icons.delete, color: Colors.white),
  ),
  onDismissed: (direction) {
    // Remove item
  },
  child: ListTile(title: Text(item.title)),
)

// Draggable
Draggable<String>(
  data: 'Item data',
  child: Container(
    width: 100,
    height: 100,
    color: Colors.blue,
    child: Center(child: Text('Drag me')),
  ),
  feedback: Material(
    elevation: 4,
    child: Container(
      width: 100,
      height: 100,
      color: Colors.blue.withOpacity(0.5),
      child: Center(child: Text('Dragging')),
    ),
  ),
  childWhenDragging: Container(
    width: 100,
    height: 100,
    color: Colors.grey,
  ),
)

// DragTarget
DragTarget<String>(
  builder: (context, candidateData, rejectedData) {
    return Container(
      width: 200,
      height: 200,
      color: candidateData.isEmpty ? Colors.grey : Colors.green,
      child: Center(child: Text('Drop here')),
    );
  },
  onWillAccept: (data) => true,
  onAccept: (data) {
    print('Received: $data');
  },
)
```

### State Management

```dart
// StatefulWidget
class CounterWidget extends StatefulWidget {
  @override
  _CounterWidgetState createState() => _CounterWidgetState();
}

class _CounterWidgetState extends State<CounterWidget> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_counter'),
        ElevatedButton(
          onPressed: _incrementCounter,
          child: Text('Increment'),
        ),
      ],
    );
  }
}

// InheritedWidget
class AppState extends InheritedWidget {
  final String username;
  final VoidCallback logout;

  AppState({
    required this.username,
    required this.logout,
    required Widget child,
  }) : super(child: child);

  static AppState? of(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<AppState>();
  }

  @override
  bool updateShouldNotify(AppState oldWidget) {
    return username != oldWidget.username;
  }
}

// Usage
AppState(
  username: 'John',
  logout: () {},
  child: MyApp(),
)

// Access in child widgets
final appState = AppState.of(context);
print(appState?.username);

// ValueNotifier
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  final ValueNotifier<int> _counter = ValueNotifier<int>(0);

  @override
  void dispose() {
    _counter.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ValueListenableBuilder<int>(
          valueListenable: _counter,
          builder: (context, value, child) {
            return Text('Count: $value');
          },
        ),
        ElevatedButton(
          onPressed: () => _counter.value++,
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

### Async & Futures

```dart
// FutureBuilder
FutureBuilder<String>(
  future: fetchData(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return CircularProgressIndicator();
    }

    if (snapshot.hasError) {
      return Text('Error: ${snapshot.error}');
    }

    if (snapshot.hasData) {
      return Text('Data: ${snapshot.data}');
    }

    return Text('No data');
  },
)

// StreamBuilder
StreamBuilder<int>(
  stream: counterStream,
  initialData: 0,
  builder: (context, snapshot) {
    if (snapshot.hasError) {
      return Text('Error: ${snapshot.error}');
    }

    return Text('Count: ${snapshot.data}');
  },
)

// Example async function
Future<String> fetchData() async {
  await Future.delayed(Duration(seconds: 2));
  return 'Data loaded';
}

// Example stream
Stream<int> counterStream() async* {
  for (int i = 0; i < 10; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i;
  }
}
```

### Platform Channels

```dart
import 'package:flutter/services.dart';

// Method Channel
class BatteryService {
  static const platform = MethodChannel('samples.flutter.dev/battery');

  Future<int?> getBatteryLevel() async {
    try {
      final int? result = await platform.invokeMethod('getBatteryLevel');
      return result;
    } on PlatformException catch (e) {
      print("Failed to get battery level: '${e.message}'.");
      return null;
    }
  }
}

// Event Channel
class SensorService {
  static const eventChannel = EventChannel('samples.flutter.dev/sensor');

  Stream<double> get sensorStream {
    return eventChannel.receiveBroadcastStream().map((event) => event as double);
  }
}

// Usage
final batteryLevel = await BatteryService().getBatteryLevel();
print('Battery: $batteryLevel%');

SensorService().sensorStream.listen((value) {
  print('Sensor value: $value');
});
```

## Common Patterns

### Responsive Design

```dart
// MediaQuery
final size = MediaQuery.of(context).size;
final isPortrait = MediaQuery.of(context).orientation == Orientation.portrait;

Container(
  width: size.width * 0.8,
  height: size.height * 0.5,
)

// LayoutBuilder
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 600) {
      return TabletLayout();
    } else {
      return MobileLayout();
    }
  },
)

// OrientationBuilder
OrientationBuilder(
  builder: (context, orientation) {
    return GridView.count(
      crossAxisCount: orientation == Orientation.portrait ? 2 : 4,
      children: items,
    );
  },
)
```

### Theme Management

```dart
// Define theme
final lightTheme = ThemeData(
  primarySwatch: Colors.blue,
  brightness: Brightness.light,
  textTheme: TextTheme(
    headlineLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
    bodyMedium: TextStyle(fontSize: 16),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      padding: EdgeInsets.symmetric(horizontal: 32, vertical: 16),
    ),
  ),
);

final darkTheme = ThemeData(
  primarySwatch: Colors.blue,
  brightness: Brightness.dark,
);

// Apply theme
MaterialApp(
  theme: lightTheme,
  darkTheme: darkTheme,
  themeMode: ThemeMode.system,
  home: HomeScreen(),
)

// Access theme
final theme = Theme.of(context);
Text(
  'Styled Text',
  style: theme.textTheme.headlineLarge,
)
```

### Performance Optimization

```dart
// const constructors
const Text('Static text')
const Icon(Icons.home)

// ListView.builder for large lists (already shown above)

// RepaintBoundary
RepaintBoundary(
  child: ExpensiveWidget(),
)

// AutomaticKeepAliveClientMixin
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget>
    with AutomaticKeepAliveClientMixin {

  @override
  bool get wantKeepAlive => true;

  @override
  Widget build(BuildContext context) {
    super.build(context); // Must call
    return Container();
  }
}
```

## Resources

This skill includes reference documentation for deeper API exploration:

### references/
- `api_reference.md` - Comprehensive API reference with additional examples
- Additional library documentation can be added here

For the most up-to-date documentation, visit:
- Official API docs: https://api.flutter.dev/
- Flutter documentation: https://docs.flutter.dev/
- Widget catalog: https://docs.flutter.dev/ui/widgets

## Quick Reference

### Common Imports
```dart
import 'package:flutter/material.dart';  // Material Design
import 'package:flutter/cupertino.dart'; // iOS style
import 'package:flutter/widgets.dart';   // Base widgets
import 'package:flutter/services.dart';  // Platform services
```

### Widget Lifecycle
```dart
initState()      // Called once when widget is created
build()          // Called when widget needs to be rendered
setState()       // Trigger rebuild
dispose()        // Called when widget is removed
```

### Common Widget Properties
- `key` - Unique identifier
- `child` / `children` - Child widget(s)
- `padding` - Internal spacing
- `margin` - External spacing
- `decoration` - Visual decoration
- `constraints` - Size constraints
- `alignment` - Child alignment

### Layout Guidelines
- Use `Column` for vertical layout
- Use `Row` for horizontal layout
- Use `Stack` for overlapping widgets
- Use `Expanded` / `Flexible` for responsive sizing
- Use `ListView` for scrollable lists
- Use `GridView` for grid layouts
- Use `CustomScrollView` with Slivers for advanced scrolling
