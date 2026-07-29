from rest_framework import serializers

class LogoutSerializer(serializers.Serializer):
	refresh = serializers.CharField(
		help_text="The refresh token to blacklist"
	)

	def validate_refresh(self, value):
		from rest_framework_simplejwt.tokens import RefreshToken
		from rest_framework_simplejwt.exceptions import TokenError

		try:
			RefreshToken(self.refresh)
		except TokenError:
			raise serializers.ValidationError("Token is invalid or already blacklisted")

		return value