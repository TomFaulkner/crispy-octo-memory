import asyncio

import databases
import sqlalchemy
import ormantic as orm

database = databases.Database("mysql+pymysql://root:PASS@127.0.0.1:3306/orm_db")
metadata = sqlalchemy.MetaData()


class Note(orm.Model):
    id: orm.Integer(primary_key=True) = None
    text: orm.String(max_length=100)
    completed: orm.Boolean() = False
    number: orm.Decimal(scale=6, precision=20, max_digits=13, decimal_places=6) = '0'

    class Mapping:
        table_name = "notes"
        database = database
        metadata = metadata


async def main():
    # Create the database
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)

    async with database:

        notes = await Note.objects.all()
        print(notes)

        # .create()
        await Note.objects.create(text="Buy the groceries.", completed=False)
        await Note.objects.create(text="Call Mum.", completed=True)
        await Note.objects.create(text="Send invoices.", completed=True, number='123.0')

        # .all()
        notes = await Note.objects.all()

        # .filter()
        notes = await Note.objects.filter(completed=True).all()

        # exact, iexact, contains, icontains, lt, lte, gt, gte, in
        notes = await Note.objects.filter(text__icontains="mum").all()

        # .get()
        note = await Note.objects.get(id=1)

        # .update()
        await note.update(completed=True)

        note = await Note.objects.get(id=2)
        print(notes)


asyncio.run(main())
