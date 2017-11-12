using UnityEngine;

[System.Serializable]
public class UnitModel {
  public string key;
  public int unit_type;
  public string owner_key;
  public int health;
  public string weapon_key;
  public string armor_key;
  public int coordinate_x;
  public int coordinate_y;
  public bool has_order;
  public string current_order_key;
}
