package ibm.gse.eda;

import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;

@QuarkusTest
public class ItemSimulatorResourceTest {

    @Test
    public void testStartFunction() {
        given()
          .pathParam("numberRecords", 3)
          .when().post("http://localhost:8080/start/{numberRecords}")
          .then()
             .statusCode(200)
             .body(is("started"));
    }

}