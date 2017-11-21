using System.Collections.Generic;
using UnityEngine;

public class MapTileScript : MonoBehaviour {
  public int x;
  public int y;

  private List<TileResourceModel> resources;
  private List<ResourceTemplateModel> resource_templates;
  private BottomBarResource bottomBarResource;
  private GameSceneMain gameSceneMain;

  void Start() {
    GameObject bottomBarObject = GameObject.FindWithTag("BottomBar");
    bottomBarResource = bottomBarObject.GetComponent(typeof(BottomBarResource))
        as BottomBarResource;

    GameObject mainCamera = GameObject.FindWithTag("MainCamera");
    gameSceneMain = mainCamera.GetComponent(typeof(GameSceneMain))
        as GameSceneMain;
    GameModel gameModel = gameSceneMain.GetGameModel();
    resource_templates = gameModel.resource_templates;

  }

  void Update() {

  }

  void OnMouseUpAsButton() {
    Debug.Log("Clicked me: " + x + y);
    // Show x and y on client.
    if (bottomBarResource != null){
      int resourceType = 0;
      foreach (ResourceTemplateModel resource_template in resource_templates) {
         if (resource_template.key.Equals(resources[0].template_key)) {
            resourceType = resource_template.type;
         }
     }
      bottomBarResource.tileCoordsText.text = "x:" + x + " y:" + y;
      bottomBarResource.resourceNameText.text = "";
      bottomBarResource.resourceTypeText.text = "" + resourceType;
      bottomBarResource.saturationText.text = "" + resources[0].saturation;
    }

    foreach (TileResourceModel resource in resources) {
      Debug.Log("Resource template key: " + resource.template_key);
      Debug.Log("Resource saturation: " + resource.saturation);
    }
  }

  public void SetTileResources(List<TileResourceModel> models) {
    resources = models;
  }
}
