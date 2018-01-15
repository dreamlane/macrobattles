using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class MapTileScript : MonoBehaviour {
  private MapTileModel model;
  private List<ResourceTemplateModel> resource_templates;
  private BottomBarController bottomBarController;
  private GameSceneMain gameSceneMain;

  void Start() {
    GameObject bottomBarObject = GameObject.FindWithTag("BottomBar");
    bottomBarController =
        bottomBarObject.GetComponent(typeof(BottomBarController))
        as BottomBarController;

    GameObject mainCamera = GameObject.FindWithTag("MainCamera");
    gameSceneMain = mainCamera.GetComponent(typeof(GameSceneMain))
        as GameSceneMain;
    GameModel gameModel = gameSceneMain.GetGameModel();
    resource_templates = gameModel.resource_templates;


    bottomBarController.bottomBarButton.onClick.AddListener(SelectUnit);

  }

  void Update() {

  }

  void OnMouseUpAsButton() {
    Debug.Log("Clicked me: " + model.coordinate_x + model.coordinate_y);

    if (EventSystem.current.IsPointerOverGameObject()) {
      Debug.Log("Pointer is over a UI element, do not handle click.");
      return;
    }

    List<TileResourceModel> resources = model.resources;
    if (bottomBarController != null){
      int resourceType = 0;
      foreach (ResourceTemplateModel resource_template in resource_templates) {
         if (resource_template.key.Equals(resources[0].template_key)) {
            resourceType = resource_template.type;
         }
     }
      bottomBarController.tileCoordsText.text =
          "x:" + model.coordinate_x + " y:" + model.coordinate_y;
      bottomBarController.resourceNameText.text = "";
      bottomBarController.resourceTypeText.text = "" + resourceType;
      bottomBarController.saturationText.text = "" + resources[0].saturation;
      // if unit exists on tile
      if (model.unit_keys.Count != 0) {
        bottomBarController.bottomBarButton.gameObject.SetActive(true);
        bottomBarController.bottomBarButton.GetComponentInChildren<Text>().text = "Select Unit";
      } else {
        bottomBarController.bottomBarButton.gameObject.SetActive(false);
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
    bottomBarController.bottomBarButton.gameObject.SetActive(false);
  }
}
