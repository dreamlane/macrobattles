
public static class PlayerState {
  // The key that the server uses to uniquely identify the player.
  private static PlayerModel playerModel = null;

  public static string GetPlayerKey() {
    if (playerModel != null) {
      return playerModel.key;
    }
    return null;
  }

  public static void SetPlayerKey(string key) {
    if (playerModel != null) {
      playerModel.key = key;
    }
  }

  public static void SetPlayerModel(PlayerModel model) {
    playerModel = model;
  }

}
