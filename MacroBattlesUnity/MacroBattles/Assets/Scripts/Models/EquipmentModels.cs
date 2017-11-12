using UnityEngine;

[System.Serializable]
public class WeaponData {
  public int type;
  public int power;
  public float reliability;
}

[System.Serializable]
public class ArmorData {
  public int type;
  public int durability;
  public float damage_reduction;
}

[System.Serializable]
public class EquipmentModel {
  public string key;
  public string owner_key;
  public int type;
  public WeaponData weapon_data;
  public ArmorData armor_data;
}
