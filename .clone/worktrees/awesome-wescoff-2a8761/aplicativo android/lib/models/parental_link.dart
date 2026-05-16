class ParentalLink {
  final int id;
  final int parentId;
  final int childId;
  final String? pairingCode;
  final String status; // "pending", "active"
  final DateTime createdAt;

  const ParentalLink({
    required this.id,
    required this.parentId,
    required this.childId,
    this.pairingCode,
    required this.status,
    required this.createdAt,
  });

  factory ParentalLink.fromJson(Map<String, dynamic> json) => ParentalLink(
        id: json['id'],
        parentId: json['parent_id'],
        childId: json['child_id'],
        pairingCode: json['pairing_code'],
        status: json['status'] ?? 'pending',
        createdAt: DateTime.parse(json['created_at']),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'parent_id': parentId,
        'child_id': childId,
        'pairing_code': pairingCode,
        'status': status,
        'created_at': createdAt.toIso8601String(),
      };
}
