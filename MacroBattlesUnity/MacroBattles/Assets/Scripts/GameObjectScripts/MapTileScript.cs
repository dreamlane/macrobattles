using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MapTileScript : MonoBehaviour {
  private MapTileModel model;
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


    bottomBarResource.bottomBarButton.onClick.AddListener(SelectUnit);

  }

  void Update() {

  }

  void OnMouseUpAsButton() {
    Debug.Log("Clicked me: " + model.coordinate_x + model.coordinate_y);
    
    List<TileResourceModel> resources = model.resources;
    if (bottomBarResource != null){
      int resourceType = 0;
      foreach (ResourceTemplateModel resource_template in resource_templates) {
         if (resource_template.key.Equals(resources[0].template_key)) {
            resourceType = resource_template.type;
         }
     }
      bottomBarResource.tileCoordsText.text = 
          "x:" + model.coordinate_x + " y:" + model.coordinate_y;
      bottomBarResource.resourceNameText.text = "";
      bottomBarResource.resourceTypeText.text = "" + resourceType;
      bottomBarResource.saturationText.text = "" + resources[0].saturation;
      // if unit exists on tile
      if (model.unit_keys.Count != 0) {
        bottomBarResource.bottomBarButton.gameObject.SetActive(true);
        bottomBarResource.bottomBarButton.GetComponentInChildren<Text>().text = "Select Unit";
      } else {
        bottomBarResource.bottomBarButton.gameObject.SetActive(false);
      }
    }

    foreach (TileResourceModel resource in resources) {
      Debug.Log("Resource template key: " + resource.template_key);
      Debug.Log("Resource saturation: " + resource.saturation);
    }
  }

  public void SetModel(MapTileModel model) {
    this.model = model;
  }

  void SelectUnit() {
    Debug.Log ("Unit has been Selected");
    bottomBarResource.bottomBarButton.gameObject.SetActive(false);
  }
}
