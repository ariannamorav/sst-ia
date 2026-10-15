String? requerido(String? v) => (v == null || v.trim().isEmpty) ? 'Este campo es obligatorio' : null;
