import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:sst_ia/main.dart';
import 'package:sst_ia/services/analisis_ia_service.dart';
import 'package:sst_ia/services/analisis_service.dart';
import 'package:sst_ia/services/app_state.dart';

void main() {
  testWidgets('App carga e inicializa correctamente', (WidgetTester tester) async {
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => AppState()),
          Provider<AnalisisService>(create: (_) => ServicioAnalisisIAService()),
        ],
        child: const SstIaApp(),
      ),
    );

    // Verifica que el widget principal se renderiza
    expect(find.byType(SstIaApp), findsOneWidget);
  });
}

