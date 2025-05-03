-- Seed Catalog Service data
INSERT INTO catalog.category (id, name) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'Home Services'),
('550e8400-e29b-41d4-a716-446655440002', 'Personal Care');

INSERT INTO catalog.subcategory (id, name, category_id) VALUES
('550e8400-e29b-41d4-a716-446655440003', 'Cleaning', '550e8400-e29b-41d4-a716-446655440001'),
('550e8400-e29b-41d4-a716-446655440004', 'Haircare', '550e8400-e29b-41d4-a716-446655440002');

INSERT INTO catalog.service (id, name, subcategory_id, price, duration) VALUES
('550e8400-e29b-41d4-a716-446655440005', 'House Cleaning', '550e8400-e29b-41d4-a716-446655440003', 50.00, 120),
('550e8400-e29b-41d4-a716-446655440006', 'Haircut', '550e8400-e29b-41d4-a716-446655440004', 30.00, 60);

-- Seed Slot Service data
INSERT INTO slot.partner_slot (id, partner_id, service_id, slot_time, is_available) VALUES
('550e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440005', '2025-05-04T10:00:00', true),
('550e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440006', '2025-05-04T11:00:00', true);