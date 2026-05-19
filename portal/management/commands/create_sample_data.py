from datetime import datetime

from django.core.management.base import BaseCommand

from portal.models import Fixture, Person, Seat, SensitiveDetail, TicketAllocation


class Command(BaseCommand):
    help = "Populate sample data based on the supplied fixture/seat matrix"

    def handle(self, *args, **kwargs):
        people = ["Will", "Jimmy", "Steve", "Barney", "Tod", "Dan", "Rich", "Erik", "AN Other"]
        for name in people:
            person, _ = Person.objects.get_or_create(name=name, defaults={"short_name": name})
            SensitiveDetail.objects.get_or_create(
                person=person,
                defaults={"bank_details": f"{name} bank details placeholder"},
            )

        seats = [
            ("107", "8", "454", "Block 107 Row 8 Seat 454"),
            ("107", "8", "455", "Block 107 Row 8 Seat 455"),
            ("107", "8", "456", "Block 107 Row 8 Seat 456"),
            ("103", "25", "338", "Block 103 Row 25 Seat 338"),
            ("103", "25", "337", "Block 103 Row 25 Seat 337"),
        ]
        for block, row, seat_no, label in seats:
            Seat.objects.get_or_create(label=label, defaults={"block": block, "row": row, "seat_number": seat_no})

        fixtures = [
            ("23.11.25", "Spuds", "16:30", "4-1", "A", "96.80", ["Will", "Jimmy", "Steve", "Barney", "Tod"], ["96.80", "96.80", "96.80", "85.90", "85.90"]),
            ("26.11.25", "Bayern Munich (UCL)", "20:00", "3-1", "A", "96.80", ["Will", "Jimmy", "Steve", "Barney", "Tod"], ["96.80", "96.80", "96.80", "85.90", "85.90"]),
            ("03.12.25", "Brentford", "19:30", "2-0", "C", "39.70", ["Will", "Dan", "Tod", "Barney", "AN Other"], ["39.70", "39.70", "39.70", "35.00", "35.00"]),
            ("13.12.25", "Wolves", "20:00", "2-1", "C", "39.70", ["Will", "Dan", "Steve", "AN Other", "Tod"], ["39.70", "39.70", "39.70", "35.00", "35.00"]),
            ("27.12.25", "Brighton", "15:00", "2-1", "B", "56.90", ["Will", "Dan", "Steve", "Jimmy", "Tod"], ["56.90", "56.90", "56.90", "49.40", "49.40"]),
            ("30.12.25", "Aston Villa", "20:15", "4-1", "B", "56.90", ["Will", "Dan", "Steve", "Jimmy", "Tod"], ["56.90", "56.90", "56.90", "49.40", "49.40"]),
            ("08.01.26", "Liverpool", "20:00", "0-0", "A", "96.80", ["Will", "Dan", "Steve", "Barney", "AN Other"], ["96.80", "96.80", "96.80", "85.90", "85.90"]),
            ("25.01.26", "Man United", "16:30", "2-3", "A", "96.80", ["Will", "Dan", "Steve", "Barney", "Rich"], ["96.80", "96.80", "96.80", "85.90", "85.90"]),
            ("28.01.26", "Kairat (UCL)", "20:00", "3-2", "B", "56.90", ["Will", "Dan", "Steve", "AN Other", "AN Other"], ["56.90", "56.90", "56.90", "49.40", "49.40"]),
            ("07.02.26", "Sunderland", "15:00", "3-0", "C", "39.70", ["Will", "Rich", "Steve", "Jimmy", "Jimmy"], ["39.70", "39.70", "39.70", "35.00", "35.00"]),
            ("15.02.26", "Wigan (FA Cup)", "16:30", "4-0", "N/A", "0", ["", "", "", "", ""], ["", "", "", "", ""]),
            ("01.03.26", "Chelsea", "16:30", "2-1", "A", "96.80", ["Will", "Dan", "Steve", "Barney", "Rich"], ["96.80", "96.80", "96.80", "85.90", "85.90"]),
            ("14.03.26", "Everton", "17:30", "2-0", "B", "56.90", ["Steve", "Dan", "Steve", "Rich", "Rich"], ["56.90", "56.90", "56.90", "49.40", "49.40"]),
            ("17.03.26", "Bayer Leverkusen", "20:00", "2-0", "A", "96.80", ["AN Other", "Will", "Steve", "Tod", "Jimmy"], ["96.80", "96.80", "96.80", "85.90", "85.90"]),
            ("22.03.26", "CARABAO CUP FINAL", "16:30", "0-2", "4", "51.65", ["Will", "Tod", "Steve", "Barney", "Jimmy"], ["51.65", "51.65", "51.65", "58.25", "58.25"]),
            ("11.04.26", "Bournemouth", "12:30", "1-2", "C", "39.70", ["Will", "Dan", "Steve", "Jimmy", "AN Other"], ["39.70", "39.70", "39.70", "35.00", "35.00"]),
            ("15.04.26", "Sporting Lisbon (UCL)", "20:00", "0-0", "A", "96.80", ["Will", "Tod", "Steve", "Barney", "Jimmy"], ["96.80", "96.80", "96.80", "85.90", "85.90"]),
            ("25.04.26", "Newcastle Utd", "17:30", "1-0", "B", "56.90", ["Will", "Dan", "Jimmy", "Barney", "Tod"], ["56.90", "56.90", "56.90", "49.40", "49.40"]),
            ("02.05.26", "Fulham", "17:30", "3-0", "B", "56.90", ["Will", "Dan", "Steve", "Barney", "AN Other"], ["56.90", "56.90", "56.90", "49.40", "49.40"]),
            ("05.05.26", "Atletico Madrid (UCL)", "20:00", "1-0", "A", "96.80", ["Will", "Erik", "Steve", "Barney", "Jimmy"], ["96.80", "96.80", "96.80", "85.90", "85.90"]),
            ("18.05.26", "Burnley", "20:00", "1-0", "B", "56.90", ["Will", "Dan", "Steve", "Barney", "Rich"], ["56.90", "56.90", "56.90", "49.40", "49.40"]),
        ]

        seat_objs = list(Seat.objects.filter(active=True).order_by("label"))
        person_lookup = {p.name: p for p in Person.objects.all()}

        for dt, opp, ko, result, category, face, assignments, prices in fixtures:
            fixture, _ = Fixture.objects.get_or_create(
                date=datetime.strptime(dt, "%d.%m.%y").date(),
                opponent=opp,
                defaults={
                    "kick_off": datetime.strptime(ko, "%H:%M").time(),
                    "result": result,
                    "category": category,
                    "face_value": face if face else None,
                },
            )
            fixture.kick_off = datetime.strptime(ko, "%H:%M").time()
            fixture.result = result
            fixture.category = category
            fixture.face_value = face if face else None
            fixture.save()

            for i, seat in enumerate(seat_objs[:5]):
                assigned_name = assignments[i] if i < len(assignments) else ""
                assigned = person_lookup.get(assigned_name) if assigned_name else None
                allocation, _ = TicketAllocation.objects.get_or_create(fixture=fixture, seat=seat)
                allocation.assigned_to = assigned
                allocation.price = prices[i] if i < len(prices) and prices[i] else None
                allocation.payment_status = "paid" if assigned else "not_required"
                allocation.transfer_status = "transferred" if assigned else "not_required"
                allocation.save()

        self.stdout.write(self.style.SUCCESS("Sample data populated."))
