using UnityEngine;

[System.Serializable]
public class ResponseModel {
  public string status;
  public string error;
  public string data;
}

[System.Serializable]
public class PlayerModel {
  public string username;
}

[System.Serializable]
public class TownspersonModel {
  public string name;
  public int strength;
  public int intelligence;
  public int dexterity;
  public int goldCost;
}
