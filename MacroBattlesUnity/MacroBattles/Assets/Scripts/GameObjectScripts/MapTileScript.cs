using System.Collections.Generic;
using UnityEngine;

public class MapTileScript : MonoBehaviour {
  public int x;
  public int y;

  private List<TileResourceModel> resources;

  void Start() {

  }

  void Update() {

  }

  void OnMouseUpAsButton() {
    Debug.Log("Clicked me: " + x + y);
    foreach (TileResourceModel resource in resources) {
      Debug.Log("Resource template key: " + resource.template_key);
      Debug.Log("Resource saturation: " + resource.saturation);
    }
  }

  public void SetTileResources(List<TileResourceModel> models) {
    resources = models;
  }
}
