IMAGE ?= ns001:local
OUTPUT_ROOT ?= $(CURDIR)/outputs
GIT_SHA := $(shell git rev-parse HEAD 2>/dev/null || echo unknown)

.PHONY: build sanity smoke day-one clean

build:
	docker build --build-arg VCS_REF=$(GIT_SHA) -t $(IMAGE) .

sanity: build
	mkdir -p $(OUTPUT_ROOT)/sanity
	docker run --rm \
		-e JHTDB_TOKEN="$${JHTDB_TOKEN}" \
		-e NS001_CONTAINER_IMAGE="$(IMAGE)" \
		-v "$(OUTPUT_ROOT):/outputs" \
		$(IMAGE) protocols/sanity.json --output-dir /outputs/sanity

smoke: build
	mkdir -p $(OUTPUT_ROOT)/smoke
	docker run --rm \
		-e JHTDB_TOKEN="$${JHTDB_TOKEN}" \
		-e NS001_CONTAINER_IMAGE="$(IMAGE)" \
		-v "$(OUTPUT_ROOT):/outputs" \
		$(IMAGE) protocols/smoke.json --output-dir /outputs/smoke

day-one: build
	mkdir -p $(OUTPUT_ROOT)/day_one
	docker run --rm \
		-e JHTDB_TOKEN="$${JHTDB_TOKEN}" \
		-e NS001_CONTAINER_IMAGE="$(IMAGE)" \
		-v "$(OUTPUT_ROOT):/outputs" \
		$(IMAGE) protocols/day_one.json --output-dir /outputs/day_one

clean:
	rm -rf $(OUTPUT_ROOT)
