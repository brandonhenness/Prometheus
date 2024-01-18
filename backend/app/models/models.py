from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Date,
    Enum,
    DECIMAL,
    TEXT,
    TIME,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import BYTEA

Base = declarative_base()


class Entity(Base):
    __tablename__ = "entities"
    entity_id = Column(Integer, primary_key=True)
    entity_type = Column(
        Enum(
            "USER",
            "LOCATION",
            name="entity_type",
        ),
        nullable=False,
    )
    enabled = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    __mapper_args__ = {
        "polymorphic_identity": "entity",
        "polymorphic_on": entity_type,
    }


class User(Entity):
    __tablename__ = "users"
    entity_id = Column(
        Integer,
        ForeignKey("entities.entity_id"),
        primary_key=True,
    )
    ctclink_id = Column(String(255), unique=True)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255))
    legacy_username = Column(String(255), unique=True)
    legacy_last_login = Column(DateTime)
    osn_username = Column(String(255), unique=True)
    osn_last_login = Column(DateTime)
    user_type = Column(
        Enum(
            "INCARCERATED",
            "EMPLOYEE",
            name="user_type",
        ),
        nullable=False,
    )

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "inherit_condition": (entity_id == Entity.entity_id),
    }


class Location(Entity):
    __tablename__ = "locations"
    entity_id = Column(
        Integer,
        ForeignKey("entities.entity_id"),
        primary_key=True,
    )
    building = Column(String(255), nullable=False)
    room_number = Column(String(255), nullable=False)
    room_name = Column(String(255))

    __mapper_args__ = {
        "polymorphic_identity": "location",
        "inherit_condition": (entity_id == Entity.entity_id),
    }


class Employee(User):
    __tablename__ = "employees"
    entity_id = Column(
        Integer,
        ForeignKey("users.entity_id"),
        primary_key=True,
    )
    employee_id = Column(String(255), unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "inherit_condition": (entity_id == User.entity_id),
    }


class Facility(Base):
    __tablename__ = "facilities"
    facility_id = Column(String(3), primary_key=True)
    name = Column(String(255))
    abreviation = Column(String(255))
    address = Column(String(255))
    city = Column(String(255))
    state = Column(String(2))
    zip_code = Column(String(10))
    phone_number = Column(String(255))


class Incarcerated(User):
    __tablename__ = "incarcerated"
    entity_id = Column(
        Integer,
        ForeignKey("users.entity_id"),
        primary_key=True,
    )
    doc_number = Column(
        String(255),
        nullable=False,
        unique=True,
    )
    facility_id = Column(String(3), ForeignKey("facilities.facility_id"))
    housing_unit = Column(String(255))
    housing_cell = Column(String(255))
    estimated_release_date = Column(Date)
    counselor = Column(String(255))
    hs_diploma = Column(Boolean)

    # Relationships
    facility = relationship("Facility")

    __mapper_args__ = {
        "polymorphic_identity": "incarcerated",
        "inherit_condition": (entity_id == User.entity_id),
    }


class Student(Incarcerated):
    __tablename__ = "students"
    entity_id = Column(
        Integer,
        ForeignKey("incarcerated.entity_id"),
        primary_key=True,
    )
    program = Column(String(255))
    program_status = Column(
        Enum(
            "ENROLLED",
            "NOT_ENROLLED",
            "GRADUATED",
            "WITHDRAWN",
            "SUSPENDED",
            "EXPELLED",
            "TRANSFERRED",
            name="program_status",
        ),
        nullable=False,
        default="ENROLLED",
    )

    __mapper_args__ = {
        "polymorphic_identity": "student",
        "inherit_condition": (entity_id == Incarcerated.entity_id),
    }


class Asset(Base):
    __tablename__ = "assets"
    asset_id = Column(String(255), primary_key=True)
    asset_type = Column(
        Enum(
            "LAPTOP",
            "BOOK",
            "CALCULATOR",
            name="asset_type",
        ),
        nullable=False,
    )
    asset_cost = Column(DECIMAL(10, 2), default=0.00)
    asset_status = Column(
        Enum(
            "IN_SERVICE",
            "DECOMMISSIONED",
            "OUT_FOR_REPAIR",
            "MISSING",
            "BROKEN",
            name="asset_status",
        ),
        nullable=False,
        default="IN_SERVICE",
    )

    __mapper_args__ = {
        "polymorphic_identity": "asset",
        "polymorphic_on": asset_type,
    }


class Laptop(Asset):
    __tablename__ = "laptops"
    asset_id = Column(
        String(255),
        ForeignKey("assets.asset_id"),
        primary_key=True,
    )
    model_id = Column(
        Integer,
        ForeignKey("laptop_models.model_id"),
        nullable=False,
    )
    serial_number = Column(
        String(255),
        unique=True,
        nullable=False,
    )
    drive_serial = Column(String(255), unique=True)
    bios_version = Column(String(255))
    os_image_id = Column(Integer, ForeignKey("os_images.os_image_id"))

    # Relationships
    laptop_model = relationship("LaptopModel")
    os_image = relationship("OSImage")

    __mapper_args__ = {
        "polymorphic_identity": "laptop",
    }


class LaptopModel(Base):
    __tablename__ = "laptop_models"
    model_id = Column(Integer, primary_key=True)
    model = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    ram = Column(Integer)
    cpu = Column(String(255))
    storage = Column(Integer)


class OSImage(Base):
    __tablename__ = "os_images"
    os_image_id = Column(Integer, primary_key=True)
    os_image_name = Column(String(255), nullable=False)
    os_image_version = Column(String(255), nullable=False)
    os_image_type = Column(String(255), nullable=False)
    os_image_version = Column(String(255), nullable=False)
    os_image_build = Column(String(255))


class Software(Base):
    __tablename__ = "software"
    software_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    version = Column(String(255), nullable=False)


class OSImageSoftware(Base):
    __tablename__ = "os_images_software"
    os_image_id = Column(
        Integer,
        ForeignKey("os_images.os_image_id"),
        primary_key=True,
    )
    software_id = Column(
        Integer,
        ForeignKey("software.software_id"),
        primary_key=True,
    )

    # Relationships
    os_image = relationship("OSImage")
    software = relationship("Software")


class Book(Base):
    __tablename__ = "books"
    book_isbn = Column(
        String(255),
        nullable=False,
        primary_key=True,
    )
    book_title = Column(String(255), nullable=False)
    book_author = Column(String(255), nullable=False)
    book_publisher = Column(String(255))
    book_edition = Column(Integer)
    book_year = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "book",
    }


class Calculator(Asset):
    __tablename__ = "calculators"
    asset_id = Column(
        String(255),
        ForeignKey("assets.asset_id"),
        primary_key=True,
    )
    calculator_model = Column(String(255), nullable=False)
    calculator_serial_number = Column(String(255), unique=True)
    calculator_manufacturer = Column(String(255))
    calculator_manufacturer_date_code = Column(String(255))
    calculator_color = Column(String(255))

    __mapper_args__ = {
        "polymorphic_identity": "calculator",
    }


class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    course_prefix = Column(String(255), nullable=False)
    course_code = Column(String(255), nullable=False)
    course_name = Column(String(255), nullable=False)
    course_credits = Column(Integer)
    course_description = Column(TEXT)
    course_outcomes = Column(TEXT)

    # Relationship for prerequisites
    prerequisites = relationship(
        "Course",
        secondary="prerequisites",
        primaryjoin="Course.course_id==Prerequisite.course_id",
        secondaryjoin="Course.course_id==Prerequisite.prerequisite_id",
        backref="prerequisite_for",
    )

    __table_args__ = (UniqueConstraint("course_prefix", "course_code"),)


class Prerequisite(Base):
    __tablename__ = "prerequisites"
    course_id = Column(
        Integer,
        ForeignKey("courses.course_id"),
        primary_key=True,
    )
    prerequisite_id = Column(
        Integer,
        ForeignKey("courses.course_id"),
        primary_key=True,
    )


class Quarter(Base):
    __tablename__ = "quarters"
    quarter_id = Column(Integer, primary_key=True)
    quarter = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("quarter", "year"),)


class Schedule(Base):
    __tablename__ = "schedules"
    schedule_id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days = Column(String(255), nullable=False)
    start_time = Column(TIME, nullable=False)
    end_time = Column(TIME, nullable=False)
    location = Column(String(255), nullable=False)
    schedule_type = Column(
        Enum(
            "STUDY_HALL",
            "OFFICE_HOUR",
            "COMPUTER_LAB",
            "COURSE",
            name="schedule_type",
        ),
        nullable=False,
    )

    __mapper_args__ = {
        "polymorphic_identity": "schedule",
        "polymorphic_on": schedule_type,
    }


class StudyHallSchedule(Schedule):
    __tablename__ = "study_hall_schedules"
    schedule_id = Column(
        Integer,
        ForeignKey("schedules.schedule_id"),
        primary_key=True,
    )
    instructor = Column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "study_hall_schedule",
    }


class OfficeHourSchedule(Schedule):
    __tablename__ = "office_hour_schedules"
    schedule_id = Column(
        Integer,
        ForeignKey("schedules.schedule_id"),
        primary_key=True,
    )
    instructor = Column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "office_hour_schedule",
    }


class ComputerLabSchedule(Schedule):
    __tablename__ = "computer_lab_schedules"
    schedule_id = Column(
        Integer,
        ForeignKey("schedules.schedule_id"),
        primary_key=True,
    )
    lab_number = Column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "computer_lab_schedule",
    }


class CourseSchedule(Schedule):
    __tablename__ = "course_schedules"
    schedule_id = Column(
        Integer,
        ForeignKey("schedules.schedule_id"),
        primary_key=True,
    )
    course_id = Column(
        Integer,
        ForeignKey("courses.course_id"),
        nullable=False,
    )
    quarter_id = Column(
        Integer,
        ForeignKey("quarters.quarter_id"),
        nullable=False,
    )
    instructor = Column(String(255), nullable=False)

    # Relationships
    course = relationship("Course")
    quarter = relationship("Quarter")

    __mapper_args__ = {
        "polymorphic_identity": "course_schedule",
    }


class ScheduleSignUp(Base):
    __tablename__ = "schedule_sign_ups"
    sign_up_id = Column(Integer, primary_key=True)
    entity_id = Column(
        Integer,
        ForeignKey("entities.entity_id"),
        nullable=False,
    )
    schedule_id = Column(
        Integer,
        ForeignKey("schedules.schedule_id"),
        nullable=False,
    )

    # Relationships
    entity = relationship("Entity")
    schedule = relationship("Schedule")

    __table_args__ = (UniqueConstraint("entity_id", "schedule_id"),)


class Enrollment(Base):
    __tablename__ = "enrollments"
    entity_id = Column(
        Integer,
        ForeignKey("entities.entity_id"),
        primary_key=True,
    )
    schedule_id = Column(
        Integer,
        ForeignKey("course_schedules.schedule_id"),
        primary_key=True,
    )

    # Relationships
    entity = relationship("Entity")
    course_schedule = relationship("CourseSchedule")


class Signature(Base):
    __tablename__ = "signatures"
    signature_id = Column(Integer, primary_key=True)
    entity_id = Column(
        Integer,
        ForeignKey("entities.entity_id"),
        nullable=False,
    )
    signature_data = Column(BYTEA, nullable=False)

    # Relationship to Entity
    entity = relationship("Entity")


class BookAsset(Base):
    __tablename__ = "book_assets"
    asset_id = Column(
        String(255),
        ForeignKey("assets.asset_id"),
        primary_key=True,
    )
    book_isbn = Column(
        String(255),
        ForeignKey("books.book_isbn"),
        nullable=False,
    )
    book_number = Column(String(255))

    # Relationships
    asset = relationship("Asset")
    book = relationship("Book")

    __table_args__ = (UniqueConstraint("book_isbn", "book_number"),)


class Document(Base):
    __tablename__ = "documents"
    document_id = Column(Integer, primary_key=True)
    document_type = Column(
        Enum("AGREEMENT", "LABELS", name="document_type"),
        nullable=False,
    )
    document_printed_timestamp = Column(DateTime)
    document_signed_timestamp = Column(DateTime)
    document_file_name = Column(String(255))
    document_notes = Column(TEXT)


class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.entity_id"))
    asset_id = Column(
        String(255),
        ForeignKey("assets.asset_id"),
        nullable=False,
    )
    transaction_type = Column(
        Enum(
            "ISSUED",
            "RETURNED",
            "MISSING",
            "BROKEN",
            "SHIPPED",
            "RECEIVED",
            "DECOMMISSIONED",
            name="transaction_type",
        ),
        nullable=False,
    )
    transaction_timestamp = Column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
    )
    transaction_user = Column(
        String(255),
        nullable=False,
        default=func.current_user(),
    )
    transaction_notes = Column(TEXT)

    # Relationships
    entity = relationship("Entity")
    asset = relationship("Asset")


class TransactionDocument(Base):
    __tablename__ = "transaction_documents"
    transaction_id = Column(
        Integer,
        ForeignKey("transactions.transaction_id"),
        primary_key=True,
    )
    document_id = Column(
        Integer,
        ForeignKey("documents.document_id"),
        primary_key=True,
    )

    # Relationships
    transaction = relationship("Transaction")
    document = relationship("Document")


class MissingCharger(Base):
    __tablename__ = "missing_chargers"
    missing_charger_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"))
    report_date = Column(Date, nullable=False)
    last_issued_to = Column(Integer, ForeignKey("entities.entity_id"))

    # Relationships
    transaction = relationship("Transaction")
    last_issued_entity = relationship("Entity")


class IssuedAsset(Base):
    __tablename__ = "issued_assets"
    asset_id = Column(
        String(255),
        ForeignKey("assets.asset_id"),
        primary_key=True,
    )
    transaction_id = Column(
        Integer,
        ForeignKey("transactions.transaction_id"),
    )

    # Specify the foreign_keys for relationships
    transaction = relationship("Transaction", foreign_keys=[transaction_id])


class MissingAsset(Base):
    __tablename__ = "missing_assets"
    asset_id = Column(
        String(255),
        ForeignKey("assets.asset_id"),
        primary_key=True,
    )
    transaction_id = Column(
        Integer,
        ForeignKey("transactions.transaction_id"),
    )
    report_date = Column(Date, nullable=False)
    last_transaction_id = Column(
        Integer,
        ForeignKey("transactions.transaction_id"),
    )

    # Specify the foreign_keys for relationships
    transaction = relationship("Transaction", foreign_keys=[transaction_id])
    last_transaction = relationship("Transaction", foreign_keys=[last_transaction_id])
