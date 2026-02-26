from rest_framework.throttling import UserRateThrottle

class UserTypeRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        user = request.user

        if user.plan == "FREE":
            self.rate = '3/minute'
        elif user.plan == "PRO":
            return '5/minute'
        else:
            return None

        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)

