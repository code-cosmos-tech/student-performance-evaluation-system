from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentFeatures(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        populate_by_name=True
    )

    # academic features
    last_sem_spi: float = Field(ge=0.0, le=10.0, alias="lastSemSPI", description="Student's last semester SPI")
    internal_assessment_avg: float = Field(ge=0.0, alias="internalAssessmentAvg", description="Student's internal assessment average_score")
    attendance_percentage: float = Field(ge=0.0, le=100.0, alias="attendancePercentage", description="Student's academic attendance in percentage")
    total_backlogs: int = Field(default=0, ge=0, alias="totalBacklogs", description="Student's total number of backlogs")

    # behavioral features
    pyq_solving_frequency: int = Field(ge=0, alias="pyqSolvingFrequency", description="Student's frequency of solving PYQs")
    study_hours_weekly: float = Field(ge=0.0, alias="studyHoursWeekly", description="Student's weekly total hours of study")
    sleep_category: str = Field(alias="sleepCategory", description="Student's sleep category")
    gaming_hours_weekly: float = Field(ge=0.0, alias="gamingHoursWeekly", description="Student's weekly total gaming hours")
    assignment_delay_count: int = Field(ge=0, alias="assignmentDelayCount", description="Student's assignment delay count")

    # contextual features
    department: str = Field(alias="department", description="Student's department")
    travel_time_category: str = Field(alias="travelTimeCategory", description="Student's travel time category")
    extra_curricular_level: str = Field(alias="extraCurricularLevel", description="Student's extra curricular level")

    @field_validator('sleep_category')
    @classmethod
    def validate_sleep_category(cls, v: str) -> str:
        valid_sleep_categories = ['<6', '6-8', '>8']
        if v not in valid_sleep_categories:
            raise ValueError(
                f"Invalid sleep category '{v}'. "
                f"Valid values are {valid_sleep_categories}"
            )
        return v

    @field_validator('department')
    @classmethod
    def validate_department(cls, v: str) -> str:
        v = v.upper()
        mapping = {'CSE': 'CE', 'ECE': 'EC'}
        valid_departments = ['CE', 'IT', 'EC', 'ME', 'ICT', 'EE']

        if v in mapping:
            v = mapping[v]

        if v not in valid_departments:
            raise ValueError(
                f"Invalid department '{v}'. "
                f"Valid values are {valid_departments}"
            )
        return v

    @field_validator('travel_time_category')
    @classmethod
    def validate_travel_time_category(cls, v: str) -> str:
        valid_travel_time_categories = ['<30', '30-60', '>60']
        if v not in valid_travel_time_categories:
            raise ValueError(
                f"Invalid travel time category '{v}'. "
                f"Valid values are {valid_travel_time_categories}"
            )
        return v
    
    @field_validator('extra_curricular_level')
    @classmethod
    def validate_extra_curricular_level(cls, v: str) -> str:
        valid_extra_curricular_levels = ['Low', 'Medium', 'High']
        if v not in valid_extra_curricular_levels:
            raise ValueError(
                f"Invalid extra curricular level '{v}'. "
                f"Valid values are {valid_extra_curricular_levels}"
            )
        return v
