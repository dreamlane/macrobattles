using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class StructureModel {
  public string key;
  public string owner_key;
  public int type;
  public int health;
  public int coordinate_x;
  public int coordinate_y;
  public HarvestingCampData harvesting_camp_data;
}

[System.Serializable]
public class HarvestingCampData {
  public string tile_resource_key;
}
