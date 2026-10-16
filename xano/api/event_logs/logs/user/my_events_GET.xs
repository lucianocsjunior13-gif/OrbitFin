// Pull all event logs for the authenticated user
query "logs/user/my_events" verb=GET {
  api_group = "Event Logs"
  auth = "user"

  input {
  }

  stack {
    // Retrieve event logs for the authenticated user
    db.query event_log {
      where = $db.event_log.user_id == $auth.id
      return = {type: "list"}
    } as $user_events
  }

  response = $user_events
  tags = ["xano:quick-start"]
  guid = "oG_yiVTOJdY1Ig2pWo51bU0RxxM"
}