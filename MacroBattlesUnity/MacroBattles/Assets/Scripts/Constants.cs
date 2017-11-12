public static class Constants {
  public const string LOCAL_HOST = "localhost:8080";
  public const string APP_DOMAIN = "https://macro-battles.appspot.com";
}

public static class ResponseConstants {
  // This should stay in sync with MacroBattlesServer/requestutils.py SUCCESS_STATUS.
  public const string SUCCESS = "success";
  // This should stay in sync with MacroBattlesServer/requestutils.py FAIL_STATUS.
  public const string FAIL = "fail";
}

public static class PositionConstants {
  public const float MAP_TILE_Z = 0.0f;
  public const float STRUCTURE_Z = -1.0f;
  public const float UNIT_Z = -2.0f;
}
