import 'package:flutter_test/flutter_test.dart';
import 'package:sst_ia/main.dart';

void main() {
  testWidgets('SST-IA inicia correctamente', (WidgetTester tester) async {
    await tester.pumpWidget(const SstIaApp());
    await tester.pump();

    expect(find.byType(SstIaApp), findsOneWidget);
  });
}
