from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomFullyBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных столов"


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось забронировать стол ввиду неизвестной ошибки"


class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Время окончания брони не может быть позже времени начала брони"


class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать стол сроком более 24 часов"


class CannotAddDataToDatabase(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotProcessCSV(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл"