from datetime import datetime, timezone


class CurrentTimeTool:
	def get_current_time(self, timezone_str: str = "UTC") -> dict:
		# Only support UTC for now
		tz = (timezone_str or "UTC").upper()
		if tz != "UTC":
			raise ValueError("Only UTC timezone is supported")

		now = datetime.now(timezone.utc)
		# Format as ISO 8601 with Z
		ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
		return {"timezone": "UTC", "current_time": ts}

