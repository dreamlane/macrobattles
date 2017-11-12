using System.Collections.Generic;
using UnityEngine;


[System.Serializable]
public class MetalPropertiesModel {
  public int hardness;
  public int lustre;
  public int density;
}

[System.Serializable]
public class WoodPropertiesModel {
  public int hardness;
  public int workability;
  public int figure;
}

[System.Serializable]
public class LeatherPropertiesModel {
  public int durability;
  public int flexibility;
  public int smoothness;
}

[System.Serializable]
public class ResourceTemplateModel {
  public string key;
  public int type;
  public MetalPropertiesModel metal_properties;
  public WoodPropertiesModel wood_properties;
  public LeatherPropertiesModel leather_properties;
}

[System.Serializable]
public class ResourceModel {
  public string key;
  public string template_key;
  public int quantity;
}

