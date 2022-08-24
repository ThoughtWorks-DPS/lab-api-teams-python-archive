resource "aws_sns_topic" "team_events" {
  name = "${var.topic_name}-${var.environment}"
}
