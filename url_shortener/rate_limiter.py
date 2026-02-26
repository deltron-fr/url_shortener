from rest_framework.throttling import UserRateThrottle

class UserTypeRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        user = request.user

        if user.is_authenticated:
            if user.plan == "FREE":
                self.rate = '10/minute'
            elif user.plan == "PRO":
                self.rate = '20/minute'
            

        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)

